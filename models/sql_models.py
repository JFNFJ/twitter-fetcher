from settings import POSTGRESQL_USER, POSTGRESQL_PORT, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, POSTGRESQL_DB
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchColumnError
from passlib.hash import bcrypt

import datetime

Base = declarative_base()
engine = create_engine(f'postgresql+psycopg2://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}/{POSTGRESQL_DB}', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)

    def __init__(self, name, password, email):
        self.name = name
        self.password = bcrypt.encrypt(password)
        self.email = email

    @staticmethod
    def create_user(name, email, password):
        user = User(name=name, email=email, password=password)
        session.add(user)
        session.commit()
        return user

    def activate(self):
        self.confirmed = True
        session.add(self)
        session.commit()

    @staticmethod
    def validate_password(user, password):
        return bcrypt.verify(password, user.password)

    topics = relationship("Topic", back_populates="user", cascade="all,delete")

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', password='{self.password}')>"


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    deadline = Column(Date)
    language = Column(String)

    user = relationship("User", back_populates="topics")
    general_result = relationship("GeneralResult", uselist=False, backref="topic", cascade="all,delete")
    evolution_results = relationship("EvolutionResult", back_populates="topic", cascade="all,delete")
    location_results = relationship("LocationResult", back_populates="topic", cascade="all,delete")
    source_results = relationship("SourceResult", back_populates="topic", cascade="all,delete")

    def __repr__(self):
        return f"<Topic(name='{self.name}', deadline='{self.deadline}', " \
               f"owner='{self.user_id}', language='{self.language})>"

    @staticmethod
    def create(user_id, name, deadline, lang):
        topic = Topic(user_id=user_id, name=name, deadline=deadline, language=lang)
        session.add(topic)
        session.commit()
        return topic

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'user_id': self.user_id,
                'deadline': self.deadline.strftime('%d-%m-%Y'), 'language': self.language}


class GeneralResult(Base):
    __tablename__ = "general_results"

    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    positive = Column(Integer)
    negative = Column(Integer)
    neutral = Column(Integer)

    @staticmethod
    def create(topic_id):
        result = GeneralResult(topic_id=topic_id, positive=0, negative=0, neutral=0)
        session.add(result)
        session.commit()
        return result

    @staticmethod
    def is_in(topic_id):
        try:
            results = session.query(GeneralResult) \
                .filter(GeneralResult.topic_id == topic_id) \
                .all()
            return len(results) > 0
        except NoSuchColumnError:
            print(f"Error de columna: {topic_id}")

    def __repr__(self):
        return f"<GeneralResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}')>"

    def to_dict(self):
       return {
           'topic_id': self.topic_id,
           'positive': self.positive,
           'negative': self.negative,
           'neutral': self.neutral
       }


class EvolutionResult(Base):
    __tablename__ = "evolution_results"

    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    day = Column(Date, primary_key=True)
    positive = Column(Integer)
    negative = Column(Integer)
    neutral = Column(Integer)

    topic = relationship("Topic", back_populates="evolution_results")

    @staticmethod
    def create(topic_id, day):
        d = datetime.datetime.strptime(day, "%a %b %d %X %z %Y").date()
        result = EvolutionResult(topic_id=topic_id, day=d, positive=0, negative=0, neutral=0)
        session.add(result)
        session.commit()
        return result

    @staticmethod
    def is_in(topic_id, day):
        results = session.query(EvolutionResult) \
            .filter(EvolutionResult.topic_id == topic_id)\
            .filter(EvolutionResult.day == datetime.datetime.strptime(day, "%a %b %d %X %z %Y").date())\
            .all()
        return len(results) > 0

    def __repr__(self):
        return f"<EvolutionResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}', day='{self.day}')>"

    def to_dict(self):
       return {
           'topic_id': self.topic_id,
           'positive': self.positive,
           'negative': self.negative,
           'neutral': self.neutral,
           'day': datetime.datetime.strftime(self.day, "%d-%m-%Y")
       }


class LocationResult(Base):
    __tablename__ = "location_results"

    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    location = Column(String, primary_key=True)
    positive = Column(Integer)
    negative = Column(Integer)
    neutral = Column(Integer)

    topic = relationship("Topic", back_populates="location_results")

    @staticmethod
    def create(topic_id, location):
        result = LocationResult(topic_id=topic_id, location=location, positive=0, negative=0, neutral=0)
        session.add(result)
        session.commit()
        return result

    @staticmethod
    def is_in(topic_id, location):
        results = session.query(LocationResult) \
            .filter(LocationResult.topic_id == topic_id) \
            .filter(LocationResult.location == location) \
            .all()
        return len(results) > 0

    def __repr__(self):
        return f"<LocationResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}', location='{self.location}')>"

    def to_dict(self):
       return {
           'topic_id': self.topic_id,
           'positive': self.positive,
           'negative': self.negative,
           'neutral': self.neutral,
           'location': self.location
       }


class SourceResult(Base):
    __tablename__ = "source_results"

    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    source = Column(String, primary_key=True)
    positive = Column(Integer)
    negative = Column(Integer)
    neutral = Column(Integer)

    topic = relationship("Topic", back_populates="source_results")

    @staticmethod
    def create(topic_id, source):
        result = SourceResult(topic_id=topic_id, source=source, positive=0, negative=0, neutral=0)
        session.add(result)
        session.commit()
        return result

    @staticmethod
    def is_in(topic_id, source):
        results = session.query(SourceResult) \
            .filter(SourceResult.topic_id == topic_id) \
            .filter(SourceResult.source == source) \
            .all()
        return len(results) > 0

    def __repr__(self):
        return f"<SourceResult(topic='{self.topic}', positive='{self.positive}', " \
               f"negative='{self.negative}', neutral='{self.neutral}', source='{self.source}')>"

    def to_dict(self):
        return {
            'topic_id': self.topic_id,
            'positive': self.positive,
            'negative': self.negative,
            'neutral': self.neutral,
            'source': self.source
        }
