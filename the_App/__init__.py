from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
protocol = 'postgresql://postgres:'
password = 'Kinsman.'
host = '@localhost'
dbase = '/thefarm'
app.config['SQLALCHEMY_DATABASE_URI'] = protocol+password+host+dbase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from the_App.directory.views import directory
app.register_blueprint(directory)

db.create_all()
