from flask import Blueprint,Flask, render_template, request, flash, jsonify, make_response,redirect,url_for
from flask_login import  current_user,login_required
from . import db
from .login_decorators import user_login_required
import json
from .models import User,Maintenance_logbook, History, Employee, Student
import sqlite3

conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()


maintenance_types = ['Room Cleaning', 'Room Electric Work', 'Bathroom Maintenance']

views = Blueprint('views',__name__)


@views.route('/', methods =["GET", "POST"])
def home():

    return render_template("home.html")




@views.route("index.html", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        if request.form.get("submit_button") == "student":
            return redirect(url_for('auth.student_login'))
        elif request.form.get("submit_button") == "admin":
            return redirect(url_for('auth.admin_login'))
        elif request.form.get("submit_button") == "employee":
            return redirect(url_for('auth.employee_login'))
    
    return make_response("something went wrong")
        

@views.route('/student_dashboard', methods = ["GET", "POST"])
@login_required
def student_dashboard():
    if current_user.role !='student':
        return redirect(url_for('auth.logout'))


    if request.method == 'POST':

        complaint = request.form.get('complaint')
        if complaint == '':
            complaint = '-' 
        # maintenance_types is a list defined at the start of this file
        new_complaint = Maintenance_logbook(data = complaint,room_no=current_user.student[0].room_no,user_id=current_user.id, maintenance_type = request.form.get('my-select'))
        db.session.add(new_complaint)
        db.session.commit()
        flash("form submitted succesfully")
        return redirect(url_for('views.student_dashboard'))
    return render_template("student_dashboard.html", user=current_user)
    


@views.route('/delete/<int:id>', methods=['POST','GET'])
@login_required
def delete_note(id):


    delete_complaint = Maintenance_logbook.query.get_or_404(id)
    hist = History(data = delete_complaint.data,
                        user_id=delete_complaint.user_id, 
                        maintenance_type = delete_complaint.maintenance_type,
                         room_no=delete_complaint.room_no)
    db.session.add(hist)
    flash("hello")
    

    try:
        db.session.delete(delete_complaint)
        db.session.commit()

        return redirect(url_for('views.student_dashboard'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('views.student_dashboard'))
        
        
    

@views.route('/admin_dashboard', methods=['GET','POST'])

@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.logout'))

    if request.method == "GET":
        
        logbook = Maintenance_logbook.query.all()
        user = User.query.all()
        student = Student.query.all()

        return render_template('admin_dashboard.html', logbook=logbook, user = user, student=student)
    
    if request.method == 'POST':

        employee = Employee.query.all()
        
        for entity in employee:
            entity.min_floor = request.form.get(entity.name + '_first_select')
            entity.max_floor = request.form.get(entity.name + '_second_select')

        db.session.commit()

    return make_response('bruh you made errorrsss')
    


@views.route('/employee_dashboard', methods=['GET','POST'])
@login_required
def employee_dashboard():
    if current_user.role !='employee':
        return redirect(url_for('auth.logout'))


    no_task = 'you have no assigned task'
        
    if current_user.employee.min_floor == '-':
        return render_template('employee_dashboard.html',no_task = no_task)
        
    else:
        
        logbook = Maintenance_logbook.query.all()
        user = User.query.filter_by(id = current_user.id).first()
        # room_no=current_user.student[0].room_no
        work = current_user.employee.work
        min = int(current_user.employee.min_floor) * 100 # here 100 is multiplied so that floor ie single digit is converted to max value of a room possible in 
        max = int(current_user.employee.max_floor) * 100
            
        return render_template('employee_dashboard.html', logbook=logbook,user=user, min=min,max=max, work=work)

@views.route('/admin_assignroles', methods=['GET','POST'])
@login_required
def admin_assignroles():

    if current_user.role != 'admin':
        return redirect(url_for('auth.logout'))

    if request.method == "GET":
        
        user = User.query.all()
        logbook = Maintenance_logbook.query.all()
        employee = Employee.query.all()
        
        return render_template('admin_assignroles.html', maintenance_types=maintenance_types, logbook=logbook,user=user, employee=employee)
    
    if request.method == 'POST':
        

        employee = Employee.query.all()
        
        for entity in employee:
            entity.min_floor = request.form.get(entity.name + '_first_select')
            entity.max_floor = request.form.get(entity.name + '_second_select')

        db.session.commit()

    return redirect(url_for('views.admin_dashboard'))

        
