#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2010-2-13 -*-
import logging
from termcolor import colored

debug = True

logging.basicConfig(format="[%(asctime)s]%(message)s", level=logging.INFO)
Loger = logging.getLogger("idslog")


def info(txt):
    Loger.info(f"{colored(str(txt), 'blue')}")
    return txt


def success(txt):
    Loger.info(f"{colored(str(txt), 'green')}")
    return txt


def warning(txt):
    Loger.info(f"{colored(str(txt), 'yellow')}")
    return txt


def error(txt):
    Loger.info(f"{colored('error: ' + str(txt), 'red')}")
    return txt


def debug(txt):
    if debug:
        Loger.info(f"{colored(str(txt),'cyan')}")
    return txt


def err_exp(e):
    if debug:
        Loger.exception(e)
    return e
