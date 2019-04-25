"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_ID

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data



# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_login_logout_message(self):
        """Can add/delete if login, will not add/delete if logged out"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_ID] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp_add = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp_add.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

            resp_delete = c.post("/messages/1/delete")

            self.assertEqual(resp_delete.status_code, 302)

            msg = Message.query.all()
            self.assertFalse(msg)

        with self.client as c:
            with c.session_transaction() as sess:
                del sess[CURR_USER_ID]

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp_add = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp_add.status_code, 302)

            msg = Message.query.all()
            self.assertFalse(msg)

            resp_delete = c.post("/messages/1/delete")

            self.assertEqual(resp_delete.status_code, 302)

            msg = Message.query.all()
            self.assertFalse(msg)          

# def test_valid_message_permission(self):
