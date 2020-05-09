#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import time
import asyncio
import libpcap as pcap
import ctypes as ct
from config import device
from log import info, success, debug, warning, error  


async def collector(q=None):
    # open network interfaces
    errbuf = ct.create_string_buffer(pcap.PCAP_ERRBUF_SIZE + 1)
    pd = pcap.open_live(device, 65535, 1, 1000, errbuf)
    if not pd:
        error(f"c: pcap.open_live failed: {errbuf.value.decode('utf-8')}")
        debug(pd)
    if pcap.setnonblock(pd, 1, errbuf) == -1:
        error(f"c: pcap.setnonblock failed: {errbuf.value.decode('utf-8')}") 
    # capture data paket
    try:
        while True:
            status = pcap.dispatch(pd, -1, handle_data, ct.cast(id(q), ct.POINTER(ct.c_ubyte)))
            await asyncio.sleep(0)
    except Exception as e:
        if str(e) != '':
            error(f"c: while filed: {e}")


@pcap.pcap_handler
def handle_data(q_id_pointer, hdr, pkt):
    q = ct.cast(q_id_pointer, ct.py_object).value
    debug(f"c: caplen: {hdr.contents.caplen}")
    debug(f"c: len: {hdr.contents.len}")
    data = ct.string_at(pkt, hdr.contents.caplen)
    #debug(f'data:{data}')
    if q:
        q.put_nowait(data)
        debug(f'c: q.put done: {q.qsize()}')


# start
if __name__ == "__main__":
    try:
        asyncio.run(collector(asyncio.Queue()))
    except KeyboardInterrupt:
        info('exit]')

