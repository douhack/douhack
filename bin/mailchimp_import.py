#! /usr/bin/env python3

import os

import mailchimp

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import engine_from_config

from douhack.model import DouHackRevolutionMailChimp
from douhack.api import find_subscriber_by_email

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


config_file_path = 'config/dev/app.yml'

with open(config_file_path) as app_yml:
    _app_config = load(app_yml, Loader)

Session = scoped_session(sessionmaker())
Session.configure(bind=engine_from_config(_app_config['sqlalchemy_engine'], ''))

api_key = os.getenv('MAILCHIMP_API_KEY', _app_config.get('mailchimp_api_key'))
list_id = '3ebfbfd47d'
result_limit = 100

key_map = {
    'EMAIL': 'email',
    'FNAME': 'fname',
    'LNAME': 'lname',
    'FOOD': 'food',
    'CITY': 'city',
    'SLEEPLACE': 'sleep_place',
    'TECH': 'tech',
    'GENDER': 'gender',
    'T_SHIRT_SIZE': 't_shirt_size',
    "Їм м'ясо": 'meat',
    "Не їм м'ясо": 'vegetarian',
    'Їжа не потрібна. Живлюсь святим духом хакатона': 'none',
    'Так, буду вночі як нормальні люди спати': 'need',
    'Ні, буду кодити всю ніч': 'unneeded',
    'чоловік': 'male',
    'жінка': 'female',
    }

def get_subscribers():
    mc = mailchimp.Mailchimp(api_key)
    page_num = 0

    while True:
        lst = mc.lists.members(list_id, opts={'limit':result_limit,
                                                'start':page_num})

        for s in lst['data']:
            mrgs = {}
            for k,v in s['merges'].items():
                mrgs[key_map.get(k, k.lower())] = key_map.get(v, v)

            if mrgs.get('food') == '':
                del mrgs['food']
            if mrgs.get('sleep_place') == '':
                del mrgs['sleep_place']
            if mrgs.get('gender') == '':
                del mrgs['gender']
            if mrgs.get('t_shirt_size') == '':
                del mrgs['t_shirt_size']

            subscriber = find_subscriber_by_email(Session, mrgs['email'])
            if subscriber:
                mrgs['id'] = subscriber.id
            subscriber = DouHackRevolutionMailChimp(**mrgs)

            Session.merge(subscriber)
            Session.commit()

        if len(lst['data']) < result_limit or \
                lst['total'] - result_limit*page_num == len(lst['data']):
            break

        page_num += 1

def main():
    get_subscribers()

if __name__ == '__main__':
    main()
