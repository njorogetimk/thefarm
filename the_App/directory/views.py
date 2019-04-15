from flask import render_template, request, url_for, redirect, jsonify
from flask import Blueprint
from the_App import db, app
from the_App.directory.models import Animal, Cattle, Sheep


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

# Post Routes
@directory.route('/animal', methods=['GET', 'POST'])
def add_animal():
    name = request.form.get('name')
    family_name = request.form.get('family')
    age = request.form.get('age')
    gender = request.form.get('gender')
    family = Animal.query.filter_by(name=family_name).first()
    app.logger.info(gender)
    if not family:
        family = Animal(family_name)
    if family_name == 'Cattle':
        livestock = Cattle(name, age, gender, family)
        db.session.add(livestock)
        db.session.commit()
        return redirect(url_for('directory.get_animal', name=name, family=family_name))
    if family_name == 'Sheep':
        livestock = Sheep(name, age, gender, family)
        db.session.add(livestock)
        db.session.commit()
        return redirect(url_for('directory.get_animal', name=name, family=family_name))
    return render_template('add_animal.html')


"""
@directory.route('/feed')
def add_feed():
    pass
"""
# Update Routes
@directory.route('/update/<family>/<name>')
def updates(family, name):
    pass


# Delete Table
@directory.route('/delete/<family>/<name>')
def deleteAnimal(family, name):
    ch_family = Animal.query.filter_by(name=family).first()  # Check for family
    if not ch_family:
        return ''
    if ch_family.name == 'Cattle':
        livestock = Cattle.query.filter_by(name=name).first()
        db.session.delete(livestock)
        db.session.commit()
        return redirect(url_for('directory.get_animals'))
    if ch_family.name == 'Sheep':
        livestock = Sheep.query.filter_by(name=name).first()
        db.session.delete(livestock)
        db.session.commit()
        return redirect(url_for('directory.get_animals'))
    return str(livestock)
