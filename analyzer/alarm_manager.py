#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import asyncio
sys.path.append('..')
from log import debug


async def send_alarm(data):
    debug(f'sending the alarm')
