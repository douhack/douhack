try:
    import unittest2 as unittest
except ImportError:
    import unittest

from datetime import date, datetime

from sqlalchemy import *
from sqlalchemy.exc import *

from douhack import api
from douhack.model import User

from tests.helper import DBTestFixture, orm_session, Session


class APITest(DBTestFixture, unittest.TestCase):

    @orm_session
    def setUp(self):
        super(APITest, self).setUp()

        alice = User(displayname=u'alice',
                     email=u'alice@wonderland.com',
                     password=u'alicepassword',
                     sex='f',
                     date_of_birth=date(1985, 3, 26))

        bob = User(displayname=u'bob',
                   email=u'bob@example.com',
                   password=u'bobpassword',
                   sex='m',
                   date_of_birth=date(1978, 4, 27))

        session = Session()
        session.add_all([alice, bob])
        session.commit()

    def tearDown(self):
        super(APITest, self).tearDown()

    @orm_session
    def test_find_user_by_id(self):
        session = Session()
        alice = api.find_user_by_id(session, 1)
        self.assertEqual(alice.displayname, u"alice")
        self.assertEqual(alice.email, u"alice@wonderland.com")
        self.assertEqual(alice.sex, "f")
        self.assertEqual(alice.date_of_birth, date(1985, 3, 26))

    @orm_session
    def test_find_user_by_email(self):
        session = Session()
        alice = api.find_user_by_email(session, u"alice@wonderland.com")
        self.assertEqual(alice.displayname, u"alice")
        self.assertEqual(alice.email, u"alice@wonderland.com")
        self.assertEqual(alice.sex, u"f")
        self.assertEqual(alice.date_of_birth, datetime(1985, 3, 26).date())

    @orm_session
    def test_delete_user_by_id(self):
        session = Session()
        self.assertEqual(api.delete_user_by_id(session, 1), 1)
        self.assertIsNone(api.find_user_by_id(session, 1))
