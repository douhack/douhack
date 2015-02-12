#! /usr/bin/env python3

from sys import argv

from yaml import load, dump
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def main(db_uri):
    app_yml_config='config/prod/app.yml'
    with open(app_yml_config) as app_yml:
        _app_config = load(app_yml, Loader)
        _app_config['sqlalchemy_engine']['url'] = db_uri
        dump(_app_config, app_yml)

if __name__ == '__main__':
    main(argv[1])
