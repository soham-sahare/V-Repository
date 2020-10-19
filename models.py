from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    '''CREATE TABLE users (id SERIAL PRIMARY KEY, email VARCHAR(60) UNIQUE NOT NULL, username VARCHAR(20) UNIQUE NOT NULL, password TEXT NOT NULL);'''

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60), unique = True, nullable = False)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(), nullable=False)

class Uploads(UserMixin, db.Model):

    __tablename__ = 'uploads'

    '''CREATE TABLE uploads (upload_id SERIAL PRIMARY KEY, ids INT, name VARCHAR(30), title VARCHAR(200), source VARCHAR(30), duration VARCHAR(30), year INT, data BYTEA);'''

    upload_id = db.Column(db.Integer, primary_key = True)
    ids = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(30), nullable = False)
    title = db.Column(db.String(200), nullable = False)
    source = db.Column(db.String(30), nullable = False)
    duration = db.Column(db.String(30), nullable = False)
    year = db.Column(db.Integer, nullable = False)
    data = db.Column(db.LargeBinary)