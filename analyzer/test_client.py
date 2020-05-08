#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import ssl
import socket
import asyncio
sys.path.append('..')
from config import HOST, PORT


async def test():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations('../cert/cacert.pem')
    ssl_context.check_hostname = False
    reader, writer = await asyncio.open_connection(HOST, PORT, ssl=ssl_context)
    for _ in range(23):
        writer.write(b'aaaaa')
    writer.close()

asyncio.run(test())
