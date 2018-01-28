from flask import render_template, request, url_for, redirect, flash, session
from flask import Blueprint
from the_App import db, app
from the_App.directory.models import Animal, Cattle, Sheep, Farmer, Ranking
from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from passlib.hash import pbkdf2_sha256 as phash
from functools import wraps
import os
from werkzeug.utils import secure_filename


directory = Blueprint('directory', __name__)


@directory.route('/')
@directory.route('/home')
def home():
    return render_template('home.html')

# Get routes
@directory.route('/animals')
def get_animals():
    animals = Animal.query.all()
    return render_template('animals.html', animals=animals)


# Display a single animal
@directory.route('/animals/<family>/<name>')
def get_animal(family, name):
    if family == 'Cattle':
        livestock = Cattle.query.filter_by(name=name).first()
        return render_template('animal.html', livestock=livestock)
    if family == "Sheep":
        livestock = Sheep.query.filter_by(name=name).first()
        return render_template('animal.html', livestock=livestock)
    else:
        return redirect('directory.home', error='no family name')


"""
@directory.route('/feeds')
def get_feeds():
    pass


@directory.route('/feed/<family>')
def get_feed():
    pass
"""


# Check if logged in
def is_loggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session or 'admin' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Sign in', 'danger')
            return redirect(url_for('directory.login'))
    return wrap


# Check if is logged in as admin
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized', 'danger')
            return redirect(url_for('directory.home'))
    return wrap


# Post Routes
@directory.route('/animal', methods=['GET', 'POST'])
@is_loggedin
def add_animal():
    name = request.form.get('name')
    family_name = request.form.get('family')
    age = request.form.get('age')
    gender = request.form.get('gender')
    family = Animal.query.filter_by(name=family_name).first()
    if not family:
        family = Animal(family_name)
    if family_name == 'Cattle':
        livestock = Cattle(name, age, gender, family)
        db.session.add(livestock)
        db.session.commit()
        flash('Added {0} to the Cattle list'.format(name), 'success')
        return redirect(url_for('directory.get_animal', name=name, family=family_name))
    if family_name == 'Sheep':
        livestock = Sheep(name, age, gender, family)
        db.session.add(livestock)
        db.session.commit()
        flash('Added {0} to the Sheep list'.format(name), 'success')
        return redirect(url_for('directory.get_animal', name=name, family=family_name))
    return render_template('add_animal.html')


"""
@directory.route('/feed')
def add_feed():
    pass
"""


# Update Routes
@directory.route('/update/<family>/<name>', methods=['POST', 'GET'])
@is_loggedin
def update(family, name):
    if request.method == 'GET':
        chk_family = Animal.query.filter_by(name=family).first()  # Check family
        if not chk_family:
            return 'Flash message Family not Present'
        if chk_family.name == 'Cattle':
            chk_name = Cattle.query.filter_by(name=name).first()  # Check name
            if not chk_name:
                return 'Flash Message Animal not present'
        if chk_family.name == 'Sheep':
            chk_name = Sheep.query.filter_by(name=name).first()
            if not chk_name:
                return 'Flash Message Animal not present'
        return render_template('update.html', livestock=chk_name)
    else:
        new_name = request.form.get('name')
        age = request.form.get('age')
        if family == 'Cattle':
            livestock = Cattle.query.filter_by(name=name).first()
            livestock.name = new_name
            livestock.age = age
        if family == 'Sheep':
            livestock = Sheep.query.filter_by(name=name).first()
            livestock.name = new_name
            livestock.age = age
        db.session.commit()
        flash('{0} update successful'.format(name), 'success')
        return redirect(url_for('directory.get_animal', family=family, name=new_name))


# Delete Route
@directory.route('/delete/<family>/<name>')
@is_loggedin
def deleteAnimal(family, name):
    ch_family = Animal.query.filter_by(name=family).first()  # Check for family
    if not ch_family:
        return 'Flash Message'
    if ch_family.name == 'Cattle':
        livestock = Cattle.query.filter_by(name=name).first()
        image = livestock.imageurl
        image_path = app.config['UPLOAD_FOLDER']+image[14:]
        if os.path.exists(image_path):
            # Delete the image from the file system
            os.remove(image_path)
        db.session.delete(livestock)
        db.session.commit()
        flash('Deleted {0} from the Cattle list'.format(name), 'danger')
        return redirect(url_for('directory.get_animals'))
    if ch_family.name == 'Sheep':
        livestock = Sheep.query.filter_by(name=name).first()
        image = livestock.imageurl
        image_path = app.config['UPLOAD_FOLDER']+image[14:]
        if os.path.exists(image_path):
            # Delete the image from the file system
            os.remove(image_path)
        db.session.delete(livestock)
        db.session.commit()
        flash('Deleted {0} from the Sheep list'.format(name), 'danger')
        return redirect(url_for('directory.get_animals'))
    return str(livestock)


# Login Route Class
class RegisterForm(Form):
    name = StringField('Name', [
        validators.DataRequired(),
        validators.length(min=1, max=50)
    ])
    username = StringField('Username', [
        validators.DataRequired(),
        validators.length(min=1, max=20)
    ])
    email = EmailField('Email', [
        validators.DataRequired(),
        validators.Email()
    ])
    password = PasswordField('Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# Register Route
@directory.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = phash.hash(str(form.password.data))

        farmer = Farmer(name, username, email, password)
        db.session.add(farmer)
        db.session.commit()
        flash('You are now registered', 'success')
        return redirect(url_for('directory.login'))
    return render_template('register.html', form=form)


# Login Route
@directory.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password_get = request.form.get('password')

        farmer = Farmer.query.filter_by(username=username).first()
        if farmer:
            password = farmer.password
            verify_pass = phash.verify(password_get, password)
            if verify_pass:
                session['logged_in'] = True
                session['username'] = username
                session['imageurl'] = farmer.imageurl
                flash('You are now logged in', 'success')
                return redirect(url_for('directory.dashboard'))
            else:
                error = 'Wrong password'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Logout Route
@directory.route('/logout')
def logout():
    session.clear()
    flash('Signed Out', 'success')
    return redirect(url_for('directory.login'))


# Dashboard route
@directory.route('/dashboard')
@is_loggedin
def dashboard():
    return render_template('dashboard.html')


# UPLOADS AND ROUTE
extensions = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@directory.route('/upload/image/<model>/<name>', methods=['POST', 'GET'])
@is_loggedin
def upload(model, name):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return render_template('upload.html')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return render_template('upload.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if model == 'Sheep':
                folder = app.config['UPLOAD_FOLDER']+'/livestock/sheep'
                file.save(os.path.join(folder, filename))  # Save to filesystem
                # File path for use in imgsrc
                filepath = 'images/uploads/livestock/sheep/'+filename
                livestock = Sheep.query.filter_by(name=name).first()
                livestock.imageurl = filepath
                db.session.commit()  # save to database
                livestock = Sheep.query.filter_by(name=name).first()
                return redirect(url_for('directory.update', family='Sheep', name=livestock.name))
            elif model == 'Cattle':
                folder = app.config['UPLOAD_FOLDER']+'/livestock/cattle'
                file.save(os.path.join(folder, filename))  # Save to filesystem
                filepath = 'images/uploads/livestock/cattle/'+filename
                livestock = Cattle.query.filter_by(name=name).first()
                livestock.imageurl = filepath
                db.session.commit()  # Save to database
                livestock = Cattle.query.filter_by(name=name).first()
                return redirect(url_for('directory.update', family='Cattle', name=livestock.name))
            elif model == 'Farmer':
                folder = app.config['UPLOAD_FOLDER']+'/users'
                file.save(os.path.join(folder, filename))
                filepath = 'images/uploads/users/'+filename
                user = Farmer.query.filter_by(username=name).first()
                user.imageurl = filepath
                session['imageurl'] = user.imageurl
                db.session.commit()
                return redirect(url_for('directory.dashboard'))
            else:
                flash('Unauthorized', 'danger')
                render_template('upload.html')
    return render_template('upload.html')


# Administrator login route
@directory.route('/administrator', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password_get = request.form.get('password')
        user_query = Farmer.query.filter_by(username=username).first()
        # check if the user exists
        if user_query:
            level = user_query.level.level
        else:
            flash('Not an admin', 'danger')
            return render_template('administrator.html')
        # Check if user is an admin
        if level == 'administrator':
            password = user_query.password
            verify_pass = phash.verify(password_get, password)
            if verify_pass:
                session['admin'] = True
                session['imageurl'] = user_query.imageurl
                session['username'] = username
                session['email'] = user_query.email
                flash('Logged in', 'success')
                return redirect(url_for('directory.admin_dashboard'))
            else:
                flash('Wrong Password', 'danger')
                return render_template('administrator.html')
        else:
            flash('Not an administrator', 'danger')
            render_template('administrator.html')
    return render_template('administrator.html')


# Admin Logout Route
@directory.route('/administrator/logout')
@is_admin
def admin_logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('directory.admin'))

# Administrator dashboard
@directory.route('/administrator/dashboard')
@is_admin
def admin_dashboard():
    # Fetch all user categories
    admin = Ranking.query.filter_by(level='administrator').first()
    manager = Ranking.query.filter_by(level='manager').first()
    employee = Ranking.query.filter_by(level='employee').first()
    customer = Ranking.query.filter_by(level='customer').first()
    default = Ranking.query.filter_by(level='default').first()
    ranks = [admin, manager, employee, customer, default]
    admin_no = len([user.name for user in admin.farmer])
    manager_no = len([user.name for user in manager.farmer])
    employee_no = len([user.name for user in employee.farmer])
    customer_no = len([user.name for user in customer.farmer])
    default_no = len([user.name for user in default.farmer])
    numbers = {
        manager.level: manager_no,
        employee.level: employee_no,
        customer.level: customer_no,
        default.level: default_no,
        admin.level: admin_no
    }

    return render_template('adminDashboard.html', ranks=ranks, numbers=numbers)


# Individual levels
@directory.route('/administrator/<level>')
@is_admin
def indi_level(level):
    # Individual level
    users = Ranking.query.filter_by(level=level).first()
    if not users:
        flash('The level %s is not present' % level, 'danger')
        return redirect(url_for('directory.admin_dashboard'))
    return render_template('adminLevel.html', users=users)


# Display Individual User in a level
@directory.route('/administrator/<level>/<username>')
@is_admin
def indi_user(level, username):
    # Individual user
    level = Ranking.query.filter_by(level=level).first()
    user = Farmer.query.filter_by(username=username).first()
    if not user:
        flash('No User %s' % username, 'danger')
        return redirect(url_for('directory.admin_dashboard'))
    if not level:
        flash('No Level %s' % level, 'danger')
        return redirect(url_for('directory.admin_dashboard'))
    return render_template('adminUser.html', user=user)


# Upgrade a user to a higher level or degrade
@directory.route('/administrator/upgrade/<username>', methods=['POST'])
@is_admin
def upgrade(username):
    # Upgrade or degrade a user
    user = Farmer.query.filter_by(username=username).first()
    if not user:
        flash('The user %s is not present' % username, 'danger')
        return redirect(url_for('directory.admin_dashboard'))
    if request.method == 'POST':
        level = request.form.get('level')
        user.upgrade(level)
        db.session.commit()
        flash("%s's level has been changed to %s" % (username, level), 'success')
        return redirect(url_for('directory.indi_user', level=level, username=username))
    else:
        return redirect(url_for('directory.admin_dashboard'))
