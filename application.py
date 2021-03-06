from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from functools import wraps
import datetime, calendar
import os

app = Flask(__name__)
app.secret_key = 'secret'

# Setting up PostgreSQL with SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Retrieve database url from command line
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# 'User' table in database
class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# 'Note' table in database
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    title = db.Column(db.String(60))
    body = db.Column(db.String(4000)) # A rather arbitrary number, check it
    date_day = db.Column(db.Integer)
    date_month = db.Column(db.Integer)
    date_year = db.Column(db.Integer)

    def __init__(self, username, title, body, date_day, date_month, date_year):
        self.username = username
        self.title = title
        self.body = body
        self.date_day = date_day
        self.date_month = date_month
        self.date_year = date_year

# Define names for the months of the year
def month_name(month_number):
    if month_number == 1:
        return 'January'
    elif month_number == 2:
        return 'February'
    elif month_number == 3:
        return 'March'
    elif month_number == 4:
        return 'April'
    elif month_number == 5:
        return 'May'
    elif month_number == 6:
        return 'June'
    elif month_number == 7:
        return 'July'
    elif month_number == 8:
        return 'August'
    elif month_number == 9:
        return 'September'
    elif month_number == 10:
        return 'October'
    elif month_number == 11:
        return 'November'
    elif month_number == 12:
        return 'December'

# Determine current date
now = datetime.datetime.now()
now_month_name = month_name(now.month)

# Index
@app.route('/')
def home():

    return make_calendar(now.month, now.year)

# About
@app.route('/about')
def about():

    return render_template('about.html', now=now, now_month_name=now_month_name)

# Select a date
@app.route('/select-date', methods=['POST'])
def select_date():

    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        return make_calendar(month, year);

# Make calendar months
@app.route('/<int:month>_<int:year>')
def make_calendar(month, year):

    # Set current month and year
    current_month = month
    current_year = year

    # Create data to populate calendar
    cal_month = calendar.monthcalendar(current_year, current_month)
    month_name_current = month_name(current_month)

    # Create data from a month before
    if current_month == 1:
        cal_month_prev = calendar.monthcalendar(current_year - 1, 12)
        month_prev = 12
        month_name_prev = month_name(month_prev)
    else:
        cal_month_prev = calendar.monthcalendar(current_year, current_month - 1)
        month_prev = current_month - 1
        month_name_prev = month_name(month_prev)

    # Create data for the next month
    if current_month == 12:
        cal_month_next = calendar.monthcalendar(current_year + 1, 1)
        month_next = 1
        month_name_next = month_name(month_next)
    else:
        cal_month_next = calendar.monthcalendar(current_year, current_month + 1)
        month_next = current_month + 1
        month_name_next = month_name(month_next)

    # Add dates from previous month to blank spaces
    for i in range(7):
        if cal_month[0][i] == 0:
            cal_month[0][i] = 32 * cal_month_prev[(len(cal_month_prev)-1)][i]

    # Add dates from next month to blank spaces
    for i in range(7):
        if cal_month[(len(cal_month)-1)][i] == 0:
            cal_month[(len(cal_month)-1)][i] = 32 * cal_month_next[0][i]

    notes = []

    if ('logged_in' in session):

        # Populate calendar with saved note titles
        notes = Note.query.filter_by(username=session['username'], date_month=current_month, date_year=current_year).all()

    return render_template('index.html', session=session, notes=notes, now=now, now_month_name=now_month_name, month_prev=month_prev, month_next=month_next, current_month=current_month, current_year=current_year,
        cal_month=cal_month, cal_month_prev=cal_month_prev, cal_month_next=cal_month_next,
        month_name_prev=month_name_prev, month_name_current=month_name_current, month_name_next=month_name_next)

# Register form class - using WTForms
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match!')
    ])
    confirm = PasswordField('Confirm Password')

# Register - still need to check unique that username is unique...
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()

        flash('You are now registered. Proceed to login.', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form, now=now, now_month_name=now_month_name)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        # Retrieve form fields
        username = request.form['username']
        password_candidate = request.form['password']

        result = User.query.filter_by(username=username).first()

        if result:
            password = result.password

            if sha256_crypt.verify(password_candidate, password):

                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return render_template('back-home.html')
            else:

                # Did not pass
                error = 'Invalid login'
                return render_template('login.html', error=error, now=now, now_month_name=now_month_name)

        else:

            error = 'Username not found'
            return render_template('login.html', error=error, now=now, now_month_name=now_month_name)

    return render_template('login.html', now=now, now_month_name=now_month_name)

# Check if user is logged in
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You must be logged in to access this page.', 'danger')
            return redirect(url_for('login'))
    return wrap

# Close any open modals and return the user to the main calendar
@app.route('/back-home')
def back_home():
    return render_template('back-home.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('home'))

# Individual date's notes
@app.route('/<int:year>-<int:month>-<int:day>')
@login_required
def date(year, month, day):

    # Display the string name for the chosen date
    selected_month_name = month_name(month)

    notes = Note.query.filter_by(username=session['username'], date_year=year, date_month=month, date_day=day).all()

    if notes:

        return render_template('date.html', notes=notes,
            year=year, month=month, selected_month_name=selected_month_name, day=day, now=now, now_month_name=now_month_name)
    else:

        # Render page but with no notes
        return render_template('date.html', year=year, month=month, selected_month_name=selected_month_name, day=day, now=now, now_month_name=now_month_name)

# Note form class
class NoteForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=60)])
    body = TextAreaField('Body')

# Create a note for a particular date
@app.route('/create-note_<int:year>-<int:month>-<int:day>', methods=['GET', 'POST'])
@login_required
def create_note(year, month, day):
    selected_month_name = month_name(month)
    form = NoteForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        note = Note(session['username'], title, body, day, month, year)
        db.session.add(note)
        db.session.commit()

        flash('Note created', 'success')
        return date(year, month, day)

    return render_template('create-note.html', form=form, year=year, month=month, selected_month_name=selected_month_name, day=day, now=now, now_month_name=now_month_name)

# Update a note for a particular date
@app.route('/edit-note_<string:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):

    note = Note.query.filter_by(id=id, username=session['username']).first()

    # Details to use on the page
    year = note.date_year
    month = note.date_month
    day = note.date_day
    selected_month_name = month_name(month)

    # Get form
    form = NoteForm(request.form)

    # Populate note form fields
    form.title.data = note.title
    form.body.data = note.body

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Write new values to the db
        note.title = title
        note.body = body
        db.session.commit()

        flash('Note updated', 'success')
        return date(year, month, day)

    return render_template('edit-note.html', form=form, year=year, month=month, selected_month_name=selected_month_name, day=day, now=now, now_month_name=now_month_name)

# Delete a particular note
@app.route('/delete-note_<string:id>')
@login_required
def delete_article(id):

    note = Note.query.filter_by(id=id, username=session['username']).first()

    year = note.date_year
    month = note.date_month
    day = note.date_day

    # Execute deletion in the database
    db.session.delete(note)
    db.session.commit()

    flash('Note deleted', 'success')
    return date(year, month, day)

if __name__ == '__main__':
    app.run(debug=True)
