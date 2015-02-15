import calendar
import os
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from hashlib import sha256

from sqlalchemy import Column, Integer, UnicodeText, Date, DateTime, String, \
    BigInteger, Enum, SmallInteger, func, text, \
    Boolean, ForeignKey
from sqlalchemy.orm import deferred, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()
metadata = Base.metadata

from sqlalchemy.types import TypeDecorator, VARCHAR
import json

import logging


logger = logging.getLogger(__name__)

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        logger.debug(value)
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        return json.loads(value) if value is not None else []

__all__ = ['User', 'Event', 'EventParticipant', 'Place', 'Invite', 'MailChimpEvents']


class EventParticipant(Base):
    """
    Class represents #douhack event participant.
    """

    __tablename__ = 'event_participation'
    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='unique_participation'),
                     )


    def __init__(self, **kwargs):
        super(EventParticipant, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False, index=True)

    register_date = Column(Date)
    accepted = Column(Boolean, default = None)
    visited = Column(Boolean, default = None)
    fields = deferred(Column(JSONEncodedDict(512)))

    users = relationship("User", backref="event_assocs")
    events = relationship("Event", backref="event_assocs")


class User(Base):
    """
    Typical User description
    """

    __tablename__ = "users"


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(35), unique=True, index=True)

    email = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(35), nullable=False)
    surname = Column(String(35), nullable=False)

    food = Column(Enum('meat', 'vegetarian', 'none', name="food"), default=None)

    city = Column(String(30), default=None, index=True)

    sleep_place = Column(Enum('need', 'unneeded', name="sleep_place"), nullable=False)
    tech = deferred(Column(UnicodeText))

    gender = Column(Enum('male', 'female', name="gender"), nullable=False)
    t_shirt_size = Column(Enum('S', 'M', 'L', 'XL', 'XXL', name="t_shirt_size"), default=None)

    _salt = Column("salt", String(12))

    @hybrid_property
    def salt(self):
        """Generates a cryptographically random salt and sets its Base64 encoded
        version to the salt column, and returns the encoded salt.
        """
        if not self.id and not self._salt:
            self._salt = b64encode(os.urandom(8))

        if isinstance(self._salt, str):
            self._salt = self._salt.encode('UTF-8')

        return self._salt

    # 64 is the length of the SHA-256 encoded string length
    _password = Column("password", String(64))

    def __encrypt_password(self, password, salt):
        """
        Encrypts the password with the given salt using SHA-256. The salt must
        be cryptographically random bytes.

        :param password: the password that was provided by the user to try and
                         authenticate. This is the clear text version that we
                         will need to match against the encrypted one in the
                         database.
        :type password: basestring

        :param salt: the salt is used to strengthen the supplied password
                     against dictionary attacks.
        :type salt: an 8-byte long cryptographically random byte string
        """

        if isinstance(password, str):
            password_bytes = password.encode("UTF-8")
        else:
            password_bytes = password

        hashed_password = sha256()
        hashed_password.update(password_bytes)
        hashed_password.update(salt)
        hashed_password = hashed_password.hexdigest()

        if not isinstance(hashed_password, str):
            hashed_password = hashed_password.decode("UTF-8")

        return hashed_password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self.__encrypt_password(password,
                                                 b64decode(str(self.salt)))

    def validate_password(self, password):
        """Check the password against existing credentials.

        :type password: str
        :param password: clear text password
        :rtype: bool
        """
        return self.password == self.__encrypt_password(password,
                                                        b64decode(str(self.salt)))

    created = Column(DateTime, default=datetime.utcnow, server_default=text("now()"), nullable=False)


class Event(Base):
    """
    Class represents #douhack event.

    e.g. DOU Hackathon: Revolution
    """

    __tablename__ = 'events'


    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String(64), nullable=False)
    title = Column(String(64), nullable=False)
    desc = deferred(Column(UnicodeText, nullable=False))
    gplus_event_id = Column(String(27), unique=True, index=True)
    host_id = Column(Integer, ForeignKey('places.id'), nullable=False, index=True)

    date = Column(Date)
    closereg = Column(Date)
    fields = deferred(Column(JSONEncodedDict(512)))
    # crutch for olostan's code
    background = Column(String(255), nullable=True)
    max_regs = Column(Integer, nullable=True, default=None)
    google_map_iframe = deferred(Column(UnicodeText, nullable=True, default=None))

    participants = relationship("EventParticipant", backref="event")
    host_org = relationship("Place", backref="events")


class Invite(Base):
    """
    Class represents an event registration invitation code.
    """

    __tablename__ = 'invites'


    def __init__(self, **kwargs):
        super(Invite, self).__init__(**kwargs)

    code = Column(String(32), autoincrement=True, primary_key=True)
    email = Column(String(64), nullable=True, default=None)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    used = Column(Boolean, nullable=False, default=False)

    event = relationship("Event", backref="invites")


class Place(Base):
    """
    Class represents locations of events.

    e.g. Digital Future
    """

    __tablename__ = 'places'


    def __init__(self, **kwargs):
        super(Place, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)

    city = Column(String(20), nullable=False, default='')
    name = Column(String(20), nullable=True, default=None)
    url = Column(String(50), nullable=False, default='')
    geo = Column(String(30), nullable=False, default='')
    logo = Column(String(255), nullable=True, default=None)

    show = Column(Boolean, nullable=False, default=False)


class MailChimpEvents(Base):
    __tablename__ = 'mailchimp_events'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String(11), nullable=False, default='')
    fired_at = Column(DateTime)
    data = deferred(Column(JSONEncodedDict(512)))


class DouHackRevolutionMailChimp(Base):
    """
    Class represents MailChimp subscription.
    """

    __tablename__ = 'douhack_revolution_mailchimp'


    def __init__(self, **kwargs):
        super(DouHackRevolutionMailChimp, self).__init__(**kwargs)

    # EMAIL|FNAME|LNAME|FOOD|CITY|SLEEPLACE|TECH
    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(64), unique=True, nullable=False, index=True)
    fname = Column(String(35), nullable=True)
    lname = Column(String(35), nullable=True)
    food = Column(Enum('meat', 'vegetarian', 'none', name="food"), default=None)
    city = Column(String(40), default=None, index=True)
    sleep_place = Column(Enum('need', 'unneeded', name="sleep_place"), default=None)
    tech = deferred(Column(UnicodeText))
    ###
    gender = Column(Enum('male', 'female', name="gender"), default=None)
    t_shirt_size = Column(Enum('S', 'M', 'L', 'XL', 'XXL', name="t_shirt_size"), default=None)
