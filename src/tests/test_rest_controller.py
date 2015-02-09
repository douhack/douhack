from datetime import date

try:
    import simplejson as json
except ImportError:
    import json
from douhack.model import *
from douhack.model import metadata

from tests.helper import orm_session, Session
from blueberrypy.testing import ControllerTestCase
@orm_session
def populate_db():
    session = Session()

    alice = User(displayname=u'alice',
                 email=u'alice@wonderland.com',
                 password=u'alicepassword',
                 sex='f',
                 phone=u"23452342",
                 birthday=date(1985, 3, 26))

    bob = User(displayname=u'bob',
               email=u'bob@example.com',
               password=u'bobpassword',
               sex='m',
               phone=u"99990000",
               birthday=date(1978, 4, 27))

    session.add(alice)
    session.add(bob)
    session.commit()

class UserRESTAPITest(ControllerTestCase):
    @orm_session
    def setUp(self):
        metadata.create_all()
        populate_db()

    @orm_session
    def tearDown(self):
        metadata.drop_all()

    def test_create_user(self):
        self.fail()

    def test_show_user(self):
        self.fail()

    def test_update_user(self):
        self.fail()

    def test_delete_user(self):
        self.fail()
