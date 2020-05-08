#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-14 -*-
import sys
import asyncio
import configparser
from scapy.all import rdpcap
sys.path.append('..')
from log import info, success, debug, warning, error


CONFIG_FILE = '/home/xuan/Documents/BYDesgin/src/config.cfg'


async def preprocessor(q=None):
    # read the config
    info('p: preprocessor start')
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE)
    DATA_DIR = None
    try:
        DATA_DIR = config.get('DEFAULT', 'DATA_DIR').encode('utf-8')
        if not DATA_DIR.endswith(b'/'):
            DATA_DIR += b'/'
    except Exception as e:
        error(f"p: configuration error: {e}")
    try:
        while True:
            if q:
                debug('p: wait for q.get()')
                filename = await q.get()
                debug(f"p: filename: {filename}")
                f = rdpcap(DATA_DIR.decode('utf-8') + filename)
            else:
                debug('p: no queue')
    except Exception as e:
        if str(e) != '':
            error(f"p: while filed: {e}")


# start
if __name__ == "__main__":
    try:
        asyncio.run(preprocessor())
    except KeyboardInterrupt:
        info('exit]')

