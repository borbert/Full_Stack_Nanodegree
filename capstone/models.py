import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Table

database_name = os.getenv('DATABASE_NAME', default='agency_app')
db_user = os.getenv('DB_USER', default='postgres')
db_pass = os.getenv('DB_PASS', default=None)
db_host = os.getenv('DB_HOST', default='localhost')
port = os.getenv('PORT', default=5432)
database_path = os.getenv(
    'DATABASE_URL', default="postgres://{}:{}@{}:{}/{}".format(
        db_user, db_pass, db_host, port, database_name))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


def return_db():
    return db


def db_drop_and_create_all():
    """
    drops the database tables and starts fresh
    can be used to initialize a clean database
    """
    db.drop_all()
    db.create_all()


'''
Models
'''


class Movies(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    release_year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    imdb_rating = Column(Float, nullable=False)

    def __init__(self, title, release_year, duration, imdb_rating):
        self.title = title
        self.release_year = release_year
        self.duration = duration
        self.imdb_rating = imdb_rating

    def add(self):
        """
        This method add a new record to the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        This method update a new record to the database
        :return:
        """
        db.session.commit()

    def delete(self):
        """
        This method deletes a record from the database
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }

    def long(self):
        return {
            "title": self.title,
            "duration": self.duration,
            "release_year": self.release_year,
            "imdb_rating": self.imdb_rating
        }

    def __repr__(self):
        return "<Movie {} {} {} {} />".format(
            self.title,
            self.release_year,
            self.imdb_rating,
            self.duration
        )


class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    full_name = Column(String(512), nullable=False, default='')
    date_of_birth = Column(Date, nullable=False)
    # gender = Column(String, default='')

    def __init__(self, name, full_name, date_of_birth):
        self.name = name
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        # self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def short(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def long(self):
        return {
            "name": self.name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.strftime("%B %d, %Y"),
            # "gender":self.gender
        }

    def full_info(self):
        return {
            "name": self.name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.strftime("%B %d, %Y")
        }

    def __repr__(self):
        return "<Actor {} {} {} />".format(
            self.name,
            self.full_name,
            self.date_of_birth
        )
