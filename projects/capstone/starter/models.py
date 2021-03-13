import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

database_name = os.getenv('DATABASE_NAME',default='listapp_dev')
db_user = os.getenv('DB_USER',default='postgres')
db_pass = os.getenv('DB_PASS',default=None)
db_host = os.getenv('DB_HOST', default='localhost')
port = os.getenv('PORT',default=5432)
database_path = os.getenv(
    'DATABASE_URL',default="postgres://{}:{}@{}:{}/{}".format(
        db_user,db_pass,db_host, port, database_name))
# "postgres://{}:{}@{}/{}".format(db_user,db_pass,db_host, database_name)

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
    migrate = Migrate(app,db)

def return_db():
    return db
    
def db_create_all():
    db.create_all()

'''
Models
'''

class Item(db.Model):
    __tablename__ = 'item'

    id = Column(db.Integer, primary_key=True)
    prod_description = db.Column(db.String)
    category = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    favorite = db.Column(db.Boolean)
    stores = db.Column(db.ARRAY(db.String()))
    barcode = db.Column(db.String(500))
    lists = db.relationship('List', backref='Items', lazy=True)

    def __repr__(self):
        return f'<Item {self.name}: ID {self.id}>'

class List(db.Model):
    __tablename__ = 'list'

    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    date_added = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime, nullable=True)
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return '<List {}{}>'.format(self.prod_id, self.store_id)

class Store(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    api = db.Column(db.Boolean)
    favorite = db.Column(db.Boolean)
    items = db.relationship('Item', backref='Stores', lazy=True)
    lists = db.relationship('List', backref='Stores', lazy=True)

    def __repr__(self):
        return '<Artist {}>'.format(self.name)
