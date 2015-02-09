try:
    import unittest2 as unittest
except ImportError:
    import unittest
from datetime import date

from sqlalchemy import *
from sqlalchemy.exc import *

from douhack.model import User

from tests.helper import DBTestFixture, orm_session, Session

class UserTest(DBTestFixture, unittest.TestCase):

    @orm_session
    def test_constructor(self):

        session = Session()

        user = User(displayname=u"alice in wonderland",
                    email=u"alice@wonderland.com",
                    password=u"wonderlandpass",
                    sex=u"m",
                    date_of_birth=date.today())

        session.add(user)
        session.commit()

    @orm_session
    def test_passwords(self):

        session = Session()

        user = User(displayname=u"displayname",
                    email=u"abc@example.com",
                    sex=u"m",
                    date_of_birth=date(1980, 1, 1))
        user.password = u"password"
        session.add(user)
        session.commit()

        self.assertTrue(user.validate_password(u"password"))
        from base64 import b64decode
        self.assertEqual(user._User__encrypt_password(u"password", b64decode(user.salt)), user.password)
