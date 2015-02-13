try:
    import simplejson as json
except ImportError:
    import json

import sys
import traceback

import cherrypy

from cherrypy import HTTPError
from cherrypy.lib import httputil as cphttputil
from blueberrypy.util import from_collection, to_collection

from douhack import api
from douhack.model import User

import functools
import sqlalchemy

from datetime import date, datetime

import logging


logger = logging.getLogger(__name__)

def auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        '''
        obj is an object with context of func
        '''
        if not cherrypy.session.get('user_id'):
            raise cherrypy.HTTPError(401)
        return func(*args, **kwargs)
    return wrapper

class REST_API_Base:
    _cp_config = {"tools.json_in.on": True}

    def create(self, **kwargs):
        raise NotImplementedError()

    def show(self, **kwargs):
        raise NotImplementedError()

    def list_all(self, **kwargs):
        raise NotImplementedError()

    def update(self, **kwargs):
        raise NotImplementedError()

    def delete(self, **kwargs):
        raise NotImplementedError()

class AuthController(REST_API_Base):

    _cp_config = {"tools.json_in.on": True}

    @cherrypy.tools.json_out()
    def login(self, **kwargs):
        req = cherrypy.request
        orm_session = req.orm_session
        params = req.json
        if 'username' in params and 'password' in params:
            user = api.find_user_by_name(orm_session, params['username'])
            if user and user.validate_password(params['password']):
                cherrypy.session['user_id'] = user.id
                return to_collection(user, excludes=("password", "salt"),
                                  sort_keys=True)
            raise HTTPError(401)
        raise HTTPError(400)

    @cherrypy.tools.json_out()
    @auth
    def logout(self, **kwargs):
        try:
            del cherrypy.session['user_id']
        except:
            raise HTTPError(404)


class UserController(REST_API_Base):

    _cp_config = {"tools.json_in.on": True}

    @cherrypy.tools.json_out()
    def create(self, **kwargs):
        '''
        `user_register`
        [POST] /user/
        '''
        req = cherrypy.request
        orm_session = req.orm_session
        user = from_collection(req.json, User())
        orm_session.add(user)
        orm_session.commit()
        cherrypy.session['user_id'] = user.id
        return to_collection(user, excludes=("password", "salt"),
                          sort_keys=True)

    @cherrypy.tools.json_out()
    def check(self, name, **kwargs):
        '''
        `user_check`
        [HEAD] /user/{name}
        '''
        user = api.find_user_by_name(cherrypy.request.orm_session,
                                    name)
        if user is None:
            raise HTTPError(404)
        return {"status":"OK", "code": 200}

    @cherrypy.tools.json_out()
    @auth
    def show(self, **kwargs):
        '''
        `user_show`
        [GET] /user/
        '''
        user = api.find_user_by_id(cherrypy.request.orm_session,
                                    cherrypy.session['user_id'])
        if user:
            return to_collection(user, excludes=("password", "salt"),
                              sort_keys=True)
        raise HTTPError(404)


class Integrations(REST_API_Base):

    #@cherrypy.tools.json_out()
    def create(self, **kwargs):
        logger.debug('Integration query')
        #return 'creating someone'
        req = cherrypy.request
        orm_session = req.orm_session
        #u = req.json['user']
        logger.debug(req)
        #user = from_collection(u, User())
        #orm_session.merge(user)
        #orm_session.commit()
        return 'OK' #to_collection(user, sort_keys=True)


# RESTful-like bindings
rest_api = cherrypy.dispatch.RoutesDispatcher()
rest_api.mapper.explicit = False

# register [1]
rest_api.connect("user_register", "/user/", UserController,
                        action="create", conditions={"method":["POST"]})
# user info
rest_api.connect("user_show", "/user/", UserController,
                        action="show", conditions={"method":["GET"]})
# user info
rest_api.connect("user_check", "/user/{name}", UserController,
                        action="check", conditions={"method":["HEAD"]})

# authenticate user
rest_api.connect("user_login", "/auth/", AuthController,
                        action="login", conditions={"method":["POST"]})
# sign out user
rest_api.connect("user_logout", "/auth/", AuthController,
                        action="logout", conditions={"method":["DELETE"]})

integrations_api = cherrypy.dispatch.RoutesDispatcher()
integrations_api.mapper.explicit = False
integrations_api.connect("add_participant", "/participants", Integrations,
                        action="create", conditions={"method":["POST"]})

# Error handlers

def generic_error_handler(status, message, traceback, version):
    """error_page.default"""

    response = cherrypy.response
    response.headers['Content-Type'] = "application/json"
    response.headers.pop('Content-Length', None)

    code, reason, _ = cphttputil.valid_status(status)
    result = {"code": code, "reason": reason, "message": message}
    if hasattr(cherrypy.request, "params"):
        params = cherrypy.request.params
        if "debug" in params and params["debug"]:
            result["traceback"] = traceback
    return json.dumps(result)

def unexpected_error_handler():
    """request.error_response"""

    (typ, value, tb) = sys.exc_info()
    if typ:
        debug = False
        if hasattr(cherrypy.request, "params"):
            params = cherrypy.request.params
            debug = "debug" in params and params["debug"]

        response = cherrypy.response
        response.headers['Content-Type'] = "application/json"
        response.headers.pop('Content-Length', None)
        content = {}

        if isinstance(typ, HTTPError):
            cherrypy._cperror.clean_headers(value.code)
            response.status = value.status
            content = {"code": value.code, "reason": value.reason, "message": value._message}
        elif isinstance(typ, (TypeError, ValueError, KeyError)):
            cherrypy._cperror.clean_headers(400)
            response.status = 400
            reason, default_message = cphttputil.response_codes[400]
            content = {"code": 400, "reason": reason, "message": value.message or default_message}

        if cherrypy.serving.request.show_tracebacks or debug:
            tb = traceback.format_exc()
            content["traceback"] = tb
        response.body = json.dumps(content)
