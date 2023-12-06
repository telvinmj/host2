from . import db
from flask_login import UserMixin, login_manager
from sqlalchemy.sql import func
from datetime import datetime



class User(db.Model, UserMixin):
    # __tablename__ = 'user'  # Custom table name, so that it can be accessed when
                             #whenever needed and no need to worry if it is User or user etc

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20))
    log = db.relationship("Maintenance_logbook",backref='user')
    # student = db.relationship("Student",backref='user')
    employee = db.relationship("Employee",backref='user',uselist=False) #it like kinda stores like a list  of all id's of maintenance_logbook which this user has created


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.Integer, nullable=False)
    # password = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship("User", backref='student')


class History(db.Model):
    # __tablename__ = 'history'


    id = db.Column(db.Integer, primary_key=True)
    maintenance_type = db.Column(db.String(100), nullable= False)
    data = db.Column(db.String(500), nullable= True)
    room_no = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    deletion_time = db.Column(db.DateTime, default=datetime.now())


class Maintenance_logbook(db.Model):
    # __tablename__ = 'maintenance_logbook'

    id = db.Column(db.Integer, primary_key=True)
    maintenance_type = db.Column(db.String(100), nullable= False)
    data = db.Column(db.String(500), nullable= True)
    room_no = db.Column(db.String(20),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    work = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(20), nullable=False)
    min_floor = db.Column(db.String(5), nullable=True)
    max_floor=db.Column(db.String(5), nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))





# class User(db.Model, UserMixin):
#     # __tablename__ = 'user'  # Custom table name, so that it can be accessed when
#                              #whenever needed and no need to worry if it is User or user etc



#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     name = db.Column(db.String(20), nullable=False)
#     room_no = db.Column(db.Integer, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     role = db.Column(db.String(20), default='student')
#     log = db.relationship("Maintenance_logbook",backref='user') #it like kinda stores like a list  of all id's of maintenance_logbook which this user has created




        
# class Maintenance_logbook(db.Model):
#     # __tablename__ = 'maintenance_logbook'

#     id = db.Column(db.Integer, primary_key=True)
#     maintenance_type = db.Column(db.String(100), nullable= False)
#     data = db.Column(db.String(500), nullable= True)
#     room_no = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

# class History(db.Model):
#     # __tablename__ = 'history'


#     id = db.Column(db.Integer, primary_key=True)
#     maintenance_type = db.Column(db.String(100), nullable= False)
#     data = db.Column(db.String(500), nullable= True)
#     room_no = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
#     deletion_time = db.Column(db.DateTime, default=datetime.now())

# class Admin(db.Model, UserMixin):
#     # __tablename__ = 'admin'


#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     # name = db.Column(db.String(20), nullable=False)
#     role = db.Column(db.String(20), default='admin')
#     password = db.Column(db.String(80), nullable=False)

#     def load_user(user_id):
#         # Load the user object from the Admin table
#         return Admin.query.get(user_id)

# class Employee(db.Model, UserMixin):

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     name = db.Column(db.String(20), nullable=False)
#     work = db.Column(db.String(20),nullable=False)
#     min_floor = db.Column(db.String(5), nullable=True)
#     max_floor=db.Column(db.String(5), nullable=True)
#     password = db.Column(db.String(80), nullable=False)
#     role = db.Column(db.String(20), default='employee')
    
