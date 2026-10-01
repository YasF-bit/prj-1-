'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student(s):
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import Course

courses = [
    ('CS', '1050', 'Computer Science 1', 4),
    ('CS', '2050', 'Computer Science 2', 4),
    ('CS', '3210', 'Principles of Programming', 4),
    ('CS', '3250', 'Software Development Methods and Tools', 4),
    ('MTH', '1410', 'Calculus 1', 4),
]

with app.app_context():
    added = 0

    for prefix, number, name, credits in courses:
        existing = db.session.get(Course, (prefix, number))
        if existing is None:
            db.session.add(Course(prefix=prefix, number=number, name=name, credits=credits))
            added += 1
    db.session.commit()
    print(f'Loaded {added} courses.')
