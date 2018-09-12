from flask_sqlalchemy import SQLAlchemy
from settings import app
from passlib.hash import bcrypt

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, password, email):
        self.name = name
        self.password = bcrypt.encrypt(password)
        self.email = email

    @staticmethod
    def create_user(name, email, password):
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    def activate(self):
        self.confirmed = True
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def validate_password(user, password):
        return bcrypt.verify(password, user.password)

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
    evolution_results = db.relationship("EvolutionResult", back_populates="topic", cascade="all,delete")
    location_results = db.relationship("LocationResult", back_populates="topic", cascade="all,delete")

    def __repr__(self):
        return f"<Topic(name='{self.name}', deadline='{self.deadline}', owner='{self.user_id}')>"

    @staticmethod
    def create(user_id, name, deadline):
        topic = Topic(user_id=user_id, name=name, deadline=deadline)
        topic.general_result = GeneralResult()
        db.session.add(topic)
        db.session.commit()
        return topic

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'user_id': self.user_id,
                'deadline': self.deadline.strftime('%d-%m-%Y')}


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

    topic = db.relationship("Topic", back_populates="evolution_results")

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

    topic = db.relationship("Topic", back_populates="location_results")

    def __repr__(self):
        return f"<EvolutionResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}', location='{self.location}')>"


