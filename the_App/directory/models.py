from the_App import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    level = db.Column(db.Integer)

    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __repr__(self):
        return '<User %s>' % self.name


class Animal(db.Model):
    """ The Animals table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Animal %s>' % self.name


class Cattle(db.Model):
    """ The Cattle table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    age = db.Column(db.Integer)  # Given in days
    gender = db.Column(db.Boolean)
    """" Relates to the Animal table"""
    animal = db.relationship('Animals', backref=db.backref('cattle', lazy='dynamic'))
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    """Relates to the Feed Table"""
    feed = db.relationship('Feed', backref=db.backref('feeds', lazy='dynamic'))
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        if gender == 'M':
            self.gender = True
        else:
            self.gender = False

    def __repr__(self):
        return '<Cattle %s>' % self.name


class Feed(db.Model):
    """The Feeds Table"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    amount = db.Column(db.Float)
