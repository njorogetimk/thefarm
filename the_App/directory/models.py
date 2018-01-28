from the_App import db


class Ranking(db.Model):
    """ The Ranking of users"""
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(30), nullable=True)

    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return "<Level %s>" % self.level


class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    imageurl = db.Column(db.String(100), nullable=True)
    level = db.relationship('Ranking', backref=db.backref('farmer', lazy='dynamic'))
    level_id = db.Column(db.Integer, db.ForeignKey('ranking.id'))

    def __init__(self, name, username, email, password, imageurl='images/logo.jpg', level='default'):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.imageurl = imageurl
        self.level = Ranking.query.filter_by(level=level).first()

    def upgrade(self, level):
        # Upgrade the rank of the user
        self.level = Ranking.query.filter_by(level=level).first()

    def __repr__(self):
        return '<User %s>' % self.username


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
    imageurl = db.Column(db.String(100), nullable=True)
    """" Relates to the Animal table"""
    animal = db.relationship('Animal', backref=db.backref('cattle', lazy='dynamic'))
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))

    def __init__(self, name, age, gender, family, imageurl='images/animal.jpg'):
        self.name = name
        self.age = age
        self.animal = family
        self.imageurl = imageurl
        if gender == 'M':
            self.gender = True
        else:
            self.gender = False

    def __repr__(self):
        return '<Cattle %s>' % self.name


class Sheep(db.Model):
    """ The Cattle table """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    age = db.Column(db.Integer)  # Given in days
    imageurl = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.Boolean)
    """" Relates to the Animal table"""
    animal = db.relationship('Animal', backref=db.backref('sheep', lazy='dynamic'))
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))

    def __init__(self, name, age, gender, family, imageurl='images/animal.jpg'):
        self.name = name
        self.age = age
        self.animal = family
        self.imageurl = imageurl
        if gender == 'M':
            self.gender = True
        else:
            self.gender = False

    def __repr__(self):
        return '<Cattle %s>' % self.name


# class Feed(db.Model):
#     """The Feeds Table"""
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(40), unique=True)
#     amount = db.Column(db.Float)
#
