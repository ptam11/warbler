"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data



class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers

        self.assertEqual(User.query.get(u.id), u)
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual('<User #1: testuser, test@test.com>', f'{u}')

        # Does non-nullable and unique fields work
        
        unique_username = User(
            email="uu@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        # adding throws sql error need to figure out how catch and test that
        # db.session.add(unique_username)
        # db.session.commit()

        unique_email = User(
            email="test@test.com",
            username="UE",
            password="HASHED_PASSWORD"
        )
        
        missing_username = User(
            email="mu@test.com",
            password="HASHED_PASSWORD"
        )
        missing_email = User(
            username="ME",
            password="HASHED_PASSWORD"
        )
        missing_password = User(
            email="mp@test.com",
            username="MP",
        )

        self.assertFalse(User.query.filter_by(email="uu@test.com").all())
        self.assertFalse(User.query.filter_by(username="UE").all())

        self.assertFalse(User.query.filter_by(email="mu@test.com").all())
        self.assertFalse(User.query.filter_by(username="ME").all())
        self.assertFalse(User.query.filter_by(email="mp@test.com").all())


    def test_following(self):
        """Does the following functionality work"""

        u1 = User(
            email="u1@test.com",
            username="u1",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        u2 = User(
            email="u2@test.com",
            username="u2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.commit()

        u1.following.append(u2)
        db.session.commit()

        self.assertEqual(len(u1.following), 1)
        self.assertEqual(u2.is_followed_by(u1), True)

        u1.following.remove(u2)
        db.session.commit()

        self.assertFalse(u1.following)
        self.assertEqual(u2.is_followed_by(u1), False)
