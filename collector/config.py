#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import configparser
import psycopg2

from log import error, info


CONFIG_FILE = './config.cfg'


config = configparser.RawConfigParser()
config.read(CONFIG_FILE)
# device
try:
    device = config.get('BASE', 'DEVICE').encode("utf-8")
    UDP_TIMEOUT = int(config.get('BASE', 'UDP_TIMEOUT'))
    TCP_TIMEOUT = int(config.get('BASE', 'TCP_TIMEOUT'))
    HOST = config.get('ANALYZER', 'HOST')
    PORT = int(config.get('ANALYZER', 'PORT'))
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

