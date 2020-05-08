#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding: utf-8 -*-
# -*- date:2020-2-17 -*-
import asyncio
from collector.collector import collector
from collector.preprocessor import preprocessor
from log import info, success, debug, warning, error


async def main():
    q = asyncio.Queue()
    tasks = []
    tasks.append(asyncio.create_task(collector(q)))
    tasks.append(asyncio.create_task(preprocessor(q)))
    #await q.join()
    #for task in tasks:
    #    task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        info('exit]')

