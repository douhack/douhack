#! /usr/bin/env python3

import os

import mailchimp

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

api_key = os.getenv('MAILCHIMP_API_KEY', _app_config.get('mailchimp_api_key'))
subscribed_list_id = '3ebfbfd47d'
registered_list_id = 'e403070fa7'
former_participants_list_id = '116e213635'
result_limit = 100

def get_subscribers():
    mc = mailchimp.Mailchimp(api_key)
    page_num = 0

    registered_entries = []
    subscribed_entries = []
    registered_users = {}
    while True:
        lst = mc.lists.members(registered_list_id, opts={'limit':result_limit,
                                                        'start':page_num})

        for l in lst['data']:
            registered_users[l['merges']['EMAIL']] = l['merges']
        #registered_entries.append([l['merges'] for l in lst['data']])
        if len(lst['data']) < result_limit or \
                lst['total'] - result_limit*page_num == len(lst['data']):
            break
        page_num += 1
    #for m in registered_entries:
    #    registered_users[m['EMAIL']] = m
    ###############################
    page_num = 0
    while True:
        lst = mc.lists.members(subscribed_list_id, opts={'limit':result_limit,
                                                        'start':page_num})

        for l in lst['data']:
            if l['email'] in registered_users:
                #print(l['email'], registered_users[l['email']], l['merges'])
                registered_users[l['email']].update(l['merges'])
        #subscribed_entries.append([l['merges'] for l in lst['data']])
        if len(lst['data']) < result_limit or \
                lst['total'] - result_limit*page_num == len(lst['data']):
            break
        page_num += 1
    ###############################
    return registered_users


def debug_participants():
    from pprint import pprint
    s = get_subscribers()
    pprint(s)

def print_participants():
    s = get_subscribers()

    for k,p in s.items():
        #print(k, p)
        print('{} {}\t{}'.format(p.get('FNAME', '[NO_NAME]'), p.get('LNAME', '[NO_SURNAME]'), p['EMAIL']))

def main():
    print_participants()

if __name__ == '__main__':
    main()
