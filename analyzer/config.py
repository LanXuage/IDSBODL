#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import configparser
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from log import error, info
from bases import Nids_protocol_type, Nids_service, Nids_flag, Nids_label


CONFIG_FILE = './config.cfg'


config = configparser.RawConfigParser()
config.read(CONFIG_FILE)
# base
try:
    HOST = config.get('ANALYZER', 'HOST')
    PORT = int(config.get('ANALYZER', 'PORT'))
    PGSQL_HOST = config.get('ANALYZER', 'DB_HOST')
    PGSQL_PORT = config.get('ANALYZER', 'DB_PORT')
    PGSQL_DB = config.get('ANALYZER', 'DB_NAME')
    PGSQL_USER = config.get('ANALYZER', 'DB_USER')
    PGSQL_PASSWD = config.get('ANALYZER', 'DB_PASSWD')
    engine = create_engine("postgresql+psycopg2://%s:%s@%s:%s/%s" % (PGSQL_USER, PGSQL_PASSWD, PGSQL_HOST, PGSQL_PORT, PGSQL_DB), pool_size=30, max_overflow=0)
    DB_SESSION = sessionmaker(bind=engine)
except Exception as e:
    error(f"cfg: configuration error: {e}")


# model
MODEL_PATH = 'model/1588223660'

# controller
ALARM_WHITE_LIST = ['normal']
