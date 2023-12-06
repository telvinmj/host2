from flask import Blueprint, render_template, redirect,url_for, make_response, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, Regexp, NumberRange
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from .models import User, Employee, Student
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth',__name__)


login_manager = LoginManager()
login_manager.init_app(auth)
login_manager.login_view = "login"


class Student_RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})
    name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "full name"})
    room_no = StringField(validators=[InputRequired()],render_kw={"placeholder":"room_no"})
    submit = SubmitField("Register")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exitsts. Please choose another one.")


class Admin_RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})
    submit = SubmitField("Register")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exitsts. Please choose another one.")


class Employee_RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})
    name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "full name"})
    work = SelectField(validators=[InputRequired()],choices=['Room Cleaning', 'Room Electric Work', 'Bathroom Maintenance'], render_kw={"placeholder": "work" })
    submit = SubmitField("Register")

    def validate_username(self,username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exitsts. Please choose another one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})

    submit = SubmitField("Login")


@auth.route('/student_register', methods = ['GET', 'POST'])
def student_register():
    form = Student_RegisterForm()
    
    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)
        room = form.room_no.data
        if not room.isdigit() or int(room) <= 0 or int(room) > 1800:
            flash("enter a valid room number")
        else:
            new_user = User(username=form.username.data, password=hashed_password, name=form.name.data,role='student')
            db.session.add(new_user)
            db.session.commit()
            new_student = Student(room_no=form.room_no.data,user_id=new_user.id)
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('auth.student_login'))

    
    
    return render_template('student_register.html', form=form)

    
@auth.route('/student_login', methods = ['GET', 'POST'])
def student_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username =form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                # return make_response(str(current_user.student))
                return render_template('student_dashboard.html', user=current_user)
    
    
    return render_template('student_login.html', form=form)


@auth.route('/admin_register', methods = ['GET', 'POST'])
def admin_register():
    form = Admin_RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, role='admin',name='admin')
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.admin_login'))
    return render_template('admin_register.html', form=form)

    
@auth.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username =form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)

                return redirect(url_for('views.admin_dashboard'))
            else:
                return make_response("your password is wrong")
    
    return render_template('admin_login.html', form=form)



@auth.route('/employee_register', methods = ['GET', 'POST'])
def employee_register():
    form = Employee_RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, username=form.username.data, password=hashed_password, role='employee')
        db.session.add(new_user)
        db.session.commit()

        new_employee = Employee(work=form.work.data,user_id = new_user.id, name = new_user.name,min_floor='-',max_floor='-')
        
        db.session.add(new_employee)
        db.session.commit()
        
        return redirect(url_for('auth.employee_login'))

    return render_template('employee_register.html', form=form)

    
@auth.route('/employee_login', methods = ['GET', 'POST'])
def employee_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username =form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('views.employee_dashboard'))
        
    return render_template('employee_login.html', form=form)



@auth.route('/logout', methods=["GET", "POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('views.home'))


























