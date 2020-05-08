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


CONFIG_FILE = '/home/xuan/Documents/BYDesgin/src/config.cfg'


config = configparser.RawConfigParser()
config.read(CONFIG_FILE)
# device
try:
    device = config.get('BASE', 'DEVICE').encode("utf-8")
    UDP_TIMEOUT = int(config.get('BASE', 'UDP_TIMEOUT'))
    TCP_TIMEOUT = int(config.get('BASE', 'TCP_TIMEOUT'))
    HOST = config.get('ANALYZER', 'HOST')
    PORT = int(config.get('ANALYZER', 'PORT'))
    PGSQL_HOST = '127.0.0.1'
    PGSQL_PORT = 5432
    PGSQL_DB = 'xuange_nids'
    PGSQL_USER = 'postgres'
    PGSQL_PASSWD = 'xuange'
    engine = create_engine("postgresql+psycopg2://%s:%s@%s:%s/%s" % (PGSQL_USER, PGSQL_PASSWD, PGSQL_HOST, PGSQL_PORT, PGSQL_DB), pool_size=30, max_overflow=0)
    DB_SESSION = sessionmaker(bind=engine)
except Exception as e:
    error(f"cfg: configuration error: {e}")
else:
    info(f"cfg: device: {device}")

# services
srvs = {}
for port in config.options('SERVICES'):
    srvs[int(port)] = config.get('SERVICES', port)
info(f'cfg: services: {srvs}')

# Sensitive files and directories
sfandds = config.get('SFandD', 'sfandds').split(' ')
info(f'cfg: Sensitive files and directories: {sfandds}')

# model
MODEL_PATH = 'model/1588223660'

# controller
ALARM_WHITE_LIST = ['normal']
