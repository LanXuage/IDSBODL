#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import asyncio
sys.path.append('..')
from controller import controller
from analyzer import analyzer
from config import HOST, PORT
from log import debug, info, error


async def main():
    info(f'ca_test: starting ca_test.')
    q = asyncio.Queue()
    tasks = []
    tasks.append(asyncio.create_task(controller(q)))
    tasks.append(asyncio.create_task(analyzer(HOST, PORT, q)))
    await asyncio.gather(*tasks, return_exceptions=True)
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        info('exit]')

