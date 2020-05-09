#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2010-2-13 -*-
import sys
import logging
from termcolor import colored

logger = logging.getLogger("IDSBODL")
logger.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(levelname)s]: %(message)s')
file_handler = logging.FileHandler('logs/output.log')
file_handler.setLevel(level=logging.DEBUG)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def info(txt):
    logger.info(f"{colored(str(txt), 'white')}")
    return txt


def success(txt):
    logger.info(f"{colored(str(txt), 'green')}")
    return txt


def warning(txt):
    logger.info(f"{colored(str(txt), 'yellow')}")
    return txt


def error(txt):
    logger.info(f"{colored(str(txt), 'red')}")
    return txt


def debug(txt):
    logger.info(f"{colored(str(txt),'cyan')}")
    return txt


def err_exp(e):
    logger.exception(e)
    return e
