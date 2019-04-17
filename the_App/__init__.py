from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
protocol = 'postgresql://postgres:'
password = 'Kinsman.'
host = '@localhost'
dbase = '/thefarm'
app.config['SQLALCHEMY_DATABASE_URI'] = protocol+password+host+dbase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Uploads
UPLOAD_FOLDER = os.getcwd()+'/the_App/static/images/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024

db = SQLAlchemy(app)

from the_App.directory.views import directory
app.register_blueprint(directory)

db.create_all()
