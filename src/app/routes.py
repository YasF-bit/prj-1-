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
# from gpa_calculator_xx import calculate_gpa
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
    return "Work in progress..."

# TODO
@app.route('/enrollments/delete/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def delete_enrollment(course_prefix, course_number):
    return "Work in progress..."

# TODO
@app.route('/enrollments/create', methods=['GET', 'POST'])
@login_required
def create_enrollment():
    form = EnrollmentForm()
    form.course.choices = []
    courses = Course.query.all()
    for course in courses:
        form.course.choices.append (
            (
                f'{course.prefix}|{course.number}',
                f'{course.prefix} {course.number} - {course.name}'
            )
        )
    if form.validate_on_submit():
        course_prefix, course_number = form.course.data.split('|')
        existing_enrollment = db.session.query(Enrollment).filter_by(
            user_id=current_user.id,
            course_prefix=course_prefix,
            course_number=course_number
        ).first()

        if existing_enrollment:
            existing_enrollment.grade = form.grade.data
        else:
            enrollment = Enrollment(
                user_id=current_user.id,
                course_prefix=course_prefix,
                course_number=course_number,
                grade=form.grade.data
            )
            db.session.add(enrollment)
        db.session.commit()
        return redirect(url_for('list_enrollments'))
    return render_template('create_enrollment.html', form=form)
