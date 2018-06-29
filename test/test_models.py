import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from unittest import TestCase
from flask_sqlalchemy import SQLAlchemy
from settings import app
from models.models import User, Topic, GeneralResult, EvolutionResult, LocationResult


class TestModels(TestCase):
    db = SQLAlchemy(app)

    def setUp(self):
        self.session = self.db.session

    def tearDown(self):
        self.session.query(GeneralResult).delete()
        self.session.query(EvolutionResult).delete()
        self.session.query(LocationResult).delete()
        self.session.query(Topic).delete()
        self.session.query(User).delete()
        self.session.commit()

    def test_user_creation(self):
        self._instantiate_user()
        self.session.commit()
        assert len(User.query.all()) == 1

    def test_user_password_validation(self):
        self._instantiate_user()
        magic = User.query.filter(User.name == "magic eight ball").one()
        assert magic.validate_password("achuras")

    def test_topic_creation(self):
        magic = self._instantiate_user()
        self.session.add(Topic(user=magic, name="Sampaoli", deadline=datetime.now()))
        self.session.commit()
        assert len(Topic.query.all()) == 1

    def test_topic_relation(self):
        magic = self._instantiate_user()
        self._instantiate_topic(magic)
        assert len(magic.topics) == 2
        assert magic.topics[0].name == "Sampaoli"
        assert magic.topics[1].name == "Seleccion"

    def test_topic_general_result_relation(self):
        magic = self._instantiate_user()
        topic_sampa, topic_seleccion = self._instantiate_topic(magic)
        result = self._instantiate_general_result(topic_sampa)
        assert result.topic.name == "Sampaoli"
        assert topic_sampa.general_result.positive == 15

    def test_topic_evolution_result_relation(self):
        magic = self._instantiate_user()
        topic_sampa, topic_seleccion = self._instantiate_topic(magic)
        self._instantiate_evolution_result(topic_sampa)
        assert EvolutionResult.query.all()[0].topic.name == "Sampaoli"
        assert len(topic_sampa.evolution_results) == 2
        assert topic_sampa.evolution_results[0].positive == 15

    def test_topic_location_result_relation(self):
        magic = self._instantiate_user()
        topic_sampa, topic_seleccion = self._instantiate_topic(magic)
        self._instantiate_location_result(topic_sampa)
        assert LocationResult.query.all()[0].topic.name == "Sampaoli"
        assert len(topic_sampa.location_results) == 2
        assert topic_sampa.location_results[0].location == "AR"

    def _instantiate_user(self):
        magic = User(name="magic eight ball", email="eighty@fatmail.com", password="achuras")
        self.session.add(magic)
        self.session.commit()
        return magic

    def _instantiate_topic(self, user):
        topic_sampa = Topic(user=user, name="Sampaoli", deadline=datetime.now())
        topic_seleccion = Topic(user=user, name="Seleccion", deadline=datetime.now())
        self.session.add(topic_sampa)
        self.session.add(topic_seleccion)
        self.session.commit()
        return topic_sampa, topic_seleccion

    def _instantiate_general_result(self, topic):
        result = GeneralResult(topic=topic, positive=15, negative=5, neutral=10)
        self.session.add(result)
        self.session.commit()
        return result

    def _instantiate_evolution_result(self, topic):
        yesterday = datetime.now() - timedelta(days=1)
        result1 = EvolutionResult(topic=topic, day=yesterday, positive=15, negative=5, neutral=10)
        result2 = EvolutionResult(topic=topic, day=datetime.now(), positive=15, negative=5, neutral=10)
        self.session.add(result1)
        self.session.add(result2)
        self.session.commit()
        return result1, result2

    def _instantiate_location_result(self, topic):
        result1 = LocationResult(topic=topic, location="AR", positive=15, negative=5, neutral=10)
        result2 = LocationResult(topic=topic, location="UY", positive=15, negative=5, neutral=10)
        self.session.add(result1)
        self.session.add(result2)
        self.session.commit()
        return result1, result2
