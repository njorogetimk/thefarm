from flask import render_template
from flask import Blueprint
# from the_App import app, db
from the_App.directory.models import Animal, Feed, User


directory = Blueprint('directory', __name__)


@directory.route('/')
@directory.route('/home')
def home():
    return render_template('home.html')
