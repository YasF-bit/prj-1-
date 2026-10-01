'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student: 
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import User, Course, Enrollment
from app.forms import SignUpForm, LoginForm, EnrollmentForm, DeleteEnrollmentForm
# TODO
from gpa_calculator_xx import calculate_gpa
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data != form.passwd_confirm.data:
            form.passwd_confirm.errors.append('Passwords do not match.')
        elif db.session.get(User, form.id.data):
            form.id.errors.append('That Id is already taken.')
        else:
            hashed = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            user = User(id=form.id.data, name=form.name.data, about=form.about.data, passwd=hashed)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.get(User, form.id.data)
        if user and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            return redirect(url_for('list_enrollments'))
        form.passwd.errors.append('Invalid Id or password.')
    return render_template('login.html', form=form)

@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

# TODO
@app.route('/enrollments')
@login_required
def list_enrollments():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    delete_form = DeleteEnrollmentForm()
    return render_template('enrollments.html', enrollments=enrollments, delete_form=delete_form, gpa = calculate_gpa(enrollments))
    
    

# TODO
@app.route('/enrollments/delete/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def delete_enrollment(course_prefix, course_number):
    return "Work in progress..."

# TODO
@app.route('/enrollments/create', methods=['GET', 'POST'])
@login_required
def create_enrollment():
    return "Work in progress..."