from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import POSTGRESQL_DB, POSTGRESQL_HOST, POSTGRESQL_PASSWORD, POSTGRESQL_PORT, POSTGRESQL_USER

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'postgresql+psycopg2://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}/{POSTGRESQL_DB}'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    topics = db.relationship("Topic", back_populates="user", cascade="all,delete")

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', password='{self.password}')>"


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    deadline = db.Column(db.Date)

    user = db.relationship("User", back_populates="topics")
    general_result = db.relationship("GeneralResult", uselist=False, backref="topic", cascade="all,delete")
    evolution_results = db.relationship("EvolutionResult", uselist=False, backref="topic", cascade="all,delete")
    location_results = db.relationship("LocationResult", uselist=False, backref="topic", cascade="all,delete")

    def __repr__(self):
        return f"<Topic(name='{self.name}', deadline='{self.deadline}', owner='{self.user_id}')>"


class GeneralResult(db.Model):
    __tablename__ = "general_results"

    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), primary_key=True)
    positive = db.Column(db.Integer)
    negative = db.Column(db.Integer)
    neutral = db.Column(db.Integer)

    def __repr__(self):
        return f"<GeneralResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}')>"


class EvolutionResult(db.Model):
    __tablename__ = "evolution_results"

    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), primary_key=True)
    day = db.Column(db.Date, primary_key=True)
    positive = db.Column(db.Integer)
    negative = db.Column(db.Integer)
    neutral = db.Column(db.Integer)

    def __repr__(self):
        return f"<EvolutionResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}', day='{self.day}')>"


class LocationResult(db.Model):
    __tablename__ = "location_results"

    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), primary_key=True)
    location = db.Column(db.String, primary_key=True)
    positive = db.Column(db.Integer)
    negative = db.Column(db.Integer)
    neutral = db.Column(db.Integer)

    def __repr__(self):
        return f"<EvolutionResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}', location='{self.location}')>"
