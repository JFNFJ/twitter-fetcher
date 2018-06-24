import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from unittest import TestCase
from flask_sqlalchemy import SQLAlchemy
from settings import app
from models.models import User, Topic


class TestModels(TestCase):
    db = SQLAlchemy(app)

    def setUp(self):
        self.session = self.db.session

    def tearDown(self):
        self.session.query(Topic).delete()
        self.session.query(User).delete()
        self.session.commit()

    def test_user_creation(self):
        self.session.add(User(name="magic eight ball", email="eighty@fatmail.com", password="achuras"))
        self.session.commit()
        assert len(User.query.all()) == 1

    def test_topic_creation(self):
        magic = User(name="magic eight ball", email="eighty@fatmail.com", password="achuras")
        self.session.add(magic)
        self.session.add(Topic(user_id=magic.id, name="Sampaoli", deadline=datetime.date.today()))
        self.session.commit()
        assert len(Topic.query.all()) == 1

    def test_topic_relation(self):
        magic = User(name="magic eight ball", email="eighty@fatmail.com", password="achuras")
        self.session.add(magic)
        self.session.add(Topic(user=magic, name="Sampaoli", deadline=datetime.date.today()))
        self.session.add(Topic(user=magic, name="Seleccion", deadline=datetime.date.today()))
        self.session.commit()
        assert len(magic.topics) == 2
