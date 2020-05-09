#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-14 -*-
import sys
import ssl
import json
import uuid
import base64
import asyncio
from scapy.all import *
from config import srvs, sfandds
from config import UDP_TIMEOUT, TCP_TIMEOUT, HOST, PORT
from log import info, success, debug, warning, error, err_exp
from handle import handle_exception


time_pool = asyncio.Queue()
s_end = -1


async def preprocessor(q=None, tcp_qs={}, udp_qs={}):
    info('p: preprocessor start')
    send_q = asyncio.Queue()
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(handle_exception)
    loop.create_task(send(send_q))
    while True:
        if q:
            debug('p: wait for q.get()')
            data_tmp = await q.get()
            debug(f"p: data_tmp: {data_tmp}")
            await processing(data_tmp, tcp_qs, udp_qs, send_q)
        else:
            error('p: no queue')
            return


async def send(send_q):
    global s_end, time_pool
    info(f'time_pool: send start')
    # Establish connection with analyzer
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations('./cert/cacert.pem')
    ssl_context.check_hostname = False
    loop = asyncio.get_running_loop()
    writer = None
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT, ssl=ssl_context)
    except ConnectionRefusedError as e:
        error(f'Failed to connect to analyzer server. ')
    while True:
        try:
            debug(f'time_pool: wait for send_q.get() = {send_q.qsize()}')
            data = await send_q.get()
            debug(f'time_pool: get a send.')
            t = data.get('time')
            if s_end < time_pool.qsize():
                while s_end >= 0 and (t - time_pool._queue[time_pool.qsize() - s_end - 1].get('time')) > 2:
                    debug(f'time_pool: s_end - 1, {t}--{time_pool._queue[s_end].get("time")}')
                    s_end -= 1 
                while time_pool.qsize() >= 100 and s_end < 99:
                    debug(f'time_pool: time_pool.get()')
                    time_pool.get_nowait()
            time_pool.put_nowait(data)
            s_end += 1
            debug(f'time_pool: t_size: {time_pool.qsize()}, s_end: {s_end}')
            while not writer:
                try:
                    await asyncio.sleep(5)
                    reader, writer = await asyncio.open_connection(HOST, PORT, ssl=ssl_context)
                except ConnectionRefusedError as e:
                    error(f'Try to connect to the analyzer server. ')
            writer.write(json.dumps(data).encode())
        except KeyboardInterrupt:
            if writer:
                writer.write(b'exit}')
                writer.close()
            return


async def processing(data, tcp_qs, udp_qs, send_q):
    e = Ether(data)
    # ip protocol judgment
    next_layer = e.payload
    debug(f'p: type: {next_layer.name}')
    if not isinstance(next_layer, NoPayload):
        if next_layer.name == 'IP' or next_layer.name == 'IPv6':
            debug(f'p: is ip protocol')
            await ip_processing(next_layer, tcp_qs, udp_qs, send_q)
        else:
            warning(f'p: Temporarily unsupported protocol: {next_layer.name}')


async def ip_processing(ip_layer, tcp_qs, udp_qs, send_q):
    next_layer = ip_layer.payload
    if not isinstance(next_layer, NoPayload):
        loop = asyncio.get_running_loop()
        if next_layer.name == 'TCP':
            await tcps_processing(next_layer, tcp_qs, send_q)
        elif next_layer.name == 'UDP':
            await udps_processing(next_layer, udp_qs, send_q)
        elif next_layer.name == 'ICMP':
            loop.create_task(icmp_processing(next_layer, send_q))
        elif next_layer.name == 'ICMPv6 Echo Reply' or next_layer.name == 'ICMPv6 Echo Request':
            await icmpv6_processing(next_layer)
        else:
            warning(f'p: Temporarily unsupported protocol: {next_layer.name}')


async def tcps_processing(tcp_layer, tcp_qs, send_q):
    debug(f'p: is tcp protocol')
    debug(f'p: tcp_flag: {str(tcp_layer.flags)}, tcp_qs: {tcp_qs}')
    # The communication service of this program is skipped to avoid death cycle.
    if tcp_layer.underlayer.dst == HOST and tcp_layer.dport == PORT:
        return
    tpuid = tcp_layer.underlayer.src + ':' + str(tcp_layer.sport) + '-' + tcp_layer.underlayer.dst + ':' + str(tcp_layer.dport)
    tmp = tcp_qs.get(tpuid)
    if not tmp:
        tpuid = tcp_layer.underlayer.dst + ':' + str(tcp_layer.dport) + '-' + tcp_layer.underlayer.src + ':' + str(tcp_layer.sport)
        tmp = tcp_qs.get(tpuid)
    if not tmp:
        # Create a new subprocess to track this new TCP connection.
        debug(f'p: new TCP.')
        tcp_qs[tpuid] = asyncio.Queue()
        tcp_qs[tpuid].put_nowait(tcp_layer)
        loop = asyncio.get_running_loop()
        loop.create_task(tcp_processing(tpuid, tcp_qs, send_q, data={'src': tcp_layer.underlayer.src, 'sport': tcp_layer.sport, 'dst': tcp_layer.underlayer.dst, 'dport': tcp_layer.dport}))
    else:
        tmp.put_nowait(tcp_layer)
        

async def tcp_processing(tpuid, tcp_qs, send_q, status={'seq': 1, 'flag': 0}, data={}):
    q = tcp_qs.get(tpuid)
    data['protocol_type'] = 'TCP'
    data['urgent'] = 0
    data['hot'] = 0
    data['src_bytes'] = 0
    data['dst_bytes'] = 0
    data['data'] = []
    if not q:
        return
    while True:
        try:
            tcp_layer = await asyncio.wait_for(q.get(), timeout=TCP_TIMEOUT)
        except asyncio.TimeoutError as e:
            data['duration'] = 0
            await fin_processing(data, tpuid, tcp_qs, send_q)
            return
        tcp_layer.underlayer.show()
        data['data'].append(base64.b64encode(bytes(tcp_layer.underlayer.underlayer)).decode())
        if tcp_layer.flags.value & 0b100000 == 0b100000:
            data['urgent'] += 1
        if tcp_layer.flags.value == 0b10:
            debug(f'p: is syn.')
            status['seq'] = tcp_layer.seq
            status['flag'] = 1
            data['service'] = await get_service_by_port(tcp_layer.dport)
            data['flag'] = 'S0'
        elif tcp_layer.flags.value & 0b100 == 0b100:
            debug(f'p: is rst.')
            f = status.get('flag')
            if f == 1:
                if tcp_layer.underlayer.src == data['src']:
                    data['flag'] = 'RSTOS0'
                else:
                    data['flag'] = 'REJ'
            elif f == 2:
                if tcp_layer.underlayer.src == data['src']:
                    data['flag'] = 'RSTO'
                else:
                    data['flag'] = 'RSTR'
            elif f == 3:
                pass
            elif f == 4:
                pass
            else:
                if tcp_layer.underlayer.dst == data['dst']:
                    data['flag'] = 'RSTRH'
            await fin_processing(data, tpuid, tcp_qs, send_q)
            start_time = status.get('start_time')
            if start_time:
                data['duration'] = int(tcp_layer.time - status['start_time'])
            else:
                data['duration'] = 0
            return
        elif tcp_layer.flags.value == 0b10010:
            debug(f'p: is synAck.')
            if status['seq'] + 1 == tcp_layer.ack:
                status['seq'] = tcp_layer.seq
        elif tcp_layer.flags.value == 0b10000:
            debug(f'p: is ack.')
            f = status.get('flag')
            if f == 1:
                if status['seq'] + 1 == tcp_layer.ack:
                    status['start_time'] = tcp_layer.time
                    status['flag'] = 2
                    data['flag'] = 'S1'
                    status['seq'] = tcp_layer.seq
            elif f == 2:
                pass
            elif f == 3:
                # normal close tcp
                if status['seq'] + 1 == tcp_layer.ack:
                    debug(f'p: normal close tcp: duration = {tcp_layer.time - status["start_time"]}')
                    data['flag'] = 'SF'
                    data['duration'] = int(tcp_layer.time - status['start_time'])
                    await fin_processing(data, tpuid, tcp_qs, send_q)
                    return
            elif f == 4:
                if status['seq'] + 1 == tcp_layer.ack:
                    status['flag'] = 3
                    status['seq'] = tcp_layer.seq
            else:
                data['flag'] = 'OTH'
        elif (tcp_layer.flags.value & 0b10001) == 0b10001:
            debug(f'p: is finAck.')
            f = status.get('flag')
            if f == 1:
                if tcp_layer.underlayer.src == data['src']:
                    data['flag'] = 'SH'
            elif f == 2:
                status['flag'] = 4
                status['seq'] = tcp_layer.seq
                if tcp_layer.underlayer.src == data['src']:
                    data['flag'] = 'S2'
                else:
                    data['flag'] = 'S3'
            elif f == 3:
                status['seq'] = tcp_layer.seq
            elif f == 4:
                if status['seq'] + 1 == tcp_layer.ack:
                    status['flag'] = 3
                    status['seq'] = tcp_layer.seq
            else:
                if tcp_layer.underlayer.src == data['src']:
                    data['flag'] = 'SHR'
                    start_time = status.get('start_time')
                    if start_time:
                        data['duration'] = int(tcp_layer.time - status['start_time'])
                    else:
                        data['duration'] = 0
                    await fin_processing(data, tpuid, tcp_qs, send_q)
                    return
        else:
            debug(f'p: is tcp data.')
            tcp_data = bytes(tcp_layer.payload)
            if tcp_layer.underlayer.src == data['src']:
                data['src_bytes'] += len(tcp_data)
            else:
                data['dst_bytes'] += len(tcp_data)
            data['hot'] += await get_one_hot(tcp_data)


async def udps_processing(udp_layer, udp_qs, send_q):
    debug(f'p: is udp protocol')
    upuid = udp_layer.underlayer.src + ':' + str(udp_layer.sport) + '-' + udp_layer.underlayer.dst + ':' + str(udp_layer.dport)
    tmp = udp_qs.get(upuid)
    if not tmp:
        upuid = udp_layer.underlayer.dst + ':' + str(udp_layer.dport) + '-' + udp_layer.underlayer.src + ':' + str(udp_layer.sport)
        tmp = udp_qs.get(upuid)
    if not tmp:
        debug(f'p: new UDP.')
        udp_qs[upuid] = asyncio.Queue()
        udp_qs[upuid].put_nowait(udp_layer)
        loop = asyncio.get_running_loop()
        loop.create_task(udp_processing(upuid, udp_qs, send_q, data={'src': udp_layer.underlayer.src, 'sport': udp_layer.sport, 'dst': udp_layer.underlayer.dst, 'dport': udp_layer.dport}))
    else:
        tmp.put_nowait(udp_layer)


async def udp_processing(upuid, udp_qs, send_q, data={}):
    q = udp_qs.get(upuid)
    data['protocol_type'] = 'UDP'
    data['urgent'] = 0
    data['hot'] = 0
    data['flag'] = 'SF'
    data['data'] = []
    data['duration'] = 0
    data['dst_bytes'] = 0
    for i in range(2):
        try:
            udp_layer = await asyncio.wait_for(q.get(), timeout=UDP_TIMEOUT)
        except asyncio.TimeoutError as e:
            debug(f'p: udp recv timeout.')
            break
        udp_data = bytes(udp_layer.payload)
        if i == 0:
            data['src_bytes'] = len(udp_data)
            data['service'] = await get_service_by_port(udp_layer.dport)
        else:
            data['dst_bytes'] = len(udp_data)
        data['hot'] += await get_one_hot(udp_data)
        data['data'].append(base64.b64encode(bytes(udp_layer.underlayer.underlayer)).decode())
    await fin_processing(data, upuid, udp_qs, send_q)


async def icmp_processing(icmp_layer, send_q):
    data = {}
    debug(f'p: is icmp protocol')
    data['src'] = icmp_layer.underlayer.src
    data['sport'] = 0
    data['dst'] = icmp_layer.underlayer.dst
    data['dport'] = 0
    data['protocol_type'] = 'ICMP'
    if icmp_layer.type == 0:
        data['service'] = 'echo-reply'
    elif icmp_layer.type == 8:
        data['service'] = 'echo-request'
    else:
        data['service'] = 'echo-other'
    data['urgent'] = 0
    data['hot'] = 0
    data['flag'] = 'SF'
    icmp_data = bytes(icmp_layer.payload)
    data['data'] = [base64.b64encode(icmp_data).decode()]
    data['duration'] = 0
    data['src_bytes'] = len(icmp_data)
    data['dst_bytes'] = 0
    data['time'] = time.time()
    await fin_processing(data, send_q=send_q)


async def icmpv6_processing(icmpv6_layer):
    debug(f'p: is icmpv6 protocol')


async def get_service_by_port(port):
    tmp = srvs.get(port)
    if tmp:
        return tmp
    else:
        warning(f'p: no this port in services: {port}')
    return 'other'


async def get_one_hot(data):
    hot = 0
    for i in sfandds:
        hot += len(re.findall(i.encode(), data))
    return hot


async def fin_processing(data=None, uid=None, qs=None, send_q=None):
    global time_pool
    try:
        if qs:
            qs.pop(uid)
    except:
        pass
    if not data.get('time'):
        data['time'] = Ether(base64.b64decode(data['data'][0])).time
    if not data.get('service'):
        data['service'] = await get_service_by_port(int(data['dport']))
    debug(f'p: data = {data}')
    # processing traffic characteristic statistics
    # in 2s
    count = 0
    srv_count = 0
    serr_count = 0
    rerr_count = 0
    srv_serr_count = 0
    srv_rerr_count = 0
    same_srv_count = 0
    diff_host_count = 0
    in2s = list(time_pool._queue)[time_pool.qsize() - s_end - 1:]
    for i in in2s:
        if i.get('dst') == data.get('dst'):
            count += 1
            if i.get('service') == data.get('service'):
                same_srv_count += 1
            if i.get('flag') in ['S0', 'SH']:
                serr_count += 1
            elif i.get('flag') == 'REJ':
                rerr_count += 1
        if i.get('service') == data.get('service'):
            srv_count += 1
            if i.get('dst') != data.get('dst'):
                diff_host_count += 1
            if i.get('flag') in ['S0', 'SH']:
                srv_serr_count += 1
            elif i.get('flag') == 'REJ':
                srv_rerr_count += 1
    data['count'] = count
    data['srv_count'] = srv_count
    if count != 0:
        data['serror_rate'] = serr_count/count
        data['rerror_rate'] = rerr_count/count
        data['same_srv_rate'] = same_srv_count/count
        data['diff_srv_rate'] = 1 - data['same_srv_rate']
    else:
        data['serror_rate'] = 0
        data['rerror_rate'] = 0
        data['same_srv_rate'] = 0
        data['diff_srv_rate'] = 0
    if srv_count != 0:
        data['srv_serror_rate'] = srv_serr_count/srv_count
        data['srv_rerror_rate'] = srv_rerr_count/srv_count
        data['srv_diff_host_rate'] = diff_host_count/srv_count
    else:
        data['srv_serror_rate'] = 0
        data['srv_rerror_rate'] = 0
        data['srv_diff_host_rate'] = 0
    in100t = list(time_pool._queue)[time_pool.qsize() - 100:]
    count = 0
    srv_count = 0
    serr_count = 0
    rerr_count = 0
    srv_serr_count = 0
    srv_rerr_count = 0
    same_srv_count = 0
    diff_host_count = 0
    same_src_port_count = 0
    dst_srv_diff_host_count = 0
    dst_host_srv_serror_count = 0
    dst_host_srv_rerror_count = 0
    for i in in100t:
        if i.get('dst') == data.get('dst'):
            count += 1
            if i.get('sport') == data.get('sport'):
                same_src_port_count += 1
            if i.get('service') == data.get('service'):
                same_srv_count += 1
                if i.get('src') != data.get('src'):
                    dst_srv_diff_host_count += 1
                if i.get('flag') in ['S0', 'SH']:
                    dst_host_srv_serror_count += 1
                elif i.get('flag') == 'REJ':
                    dst_host_srv_rerror_count += 1
            if i.get('flag') in ['S0', 'SH']:
                serr_count += 1
            elif i.get('flag') == 'REJ':
                rerr_count += 1
        if i.get('service') == data.get('service'):
            srv_count += 1
            if i.get('dst') != data.get('dst'):
                diff_host_count += 1
            if i.get('flag') in ['S0', 'SH']:
                srv_serr_count += 1
            elif i.get('flag') == 'REJ':
                srv_rerr_count += 1
    data['dst_host_count'] = count
    data['dst_host_srv_count'] = srv_count
    data['dst_host_same_srv_rate'] = same_srv_count/100
    data['dst_host_diff_srv_rate'] = 1 - data['dst_host_same_srv_rate']
    data['dst_host_same_src_port_rate'] = same_src_port_count/100
    if count != 0:
        data['dst_host_serror_rate'] = serr_count/count
        data['dst_host_rerror_rate'] = rerr_count/count
    else:
        data['dst_host_serror_rate'] = 0
        data['dst_host_rerror_rate'] = 0
    if same_srv_count != 0:
        data['dst_host_srv_diff_host_rate'] = dst_srv_diff_host_count/same_srv_count
        data['dst_host_srv_serror_rate'] = dst_host_srv_serror_count/same_srv_count
        data['dst_host_srv_rerror_rate'] = dst_host_srv_rerror_count/same_srv_count
    else:
        data['dst_host_srv_diff_host_rate'] = 0
        data['dst_host_srv_serror_rate'] = 0
        data['dst_host_srv_rerror_rate'] = 0
    # save the data.data to local and send the data_uuid
    data_list = data.pop('data')
    data['data_number'] = uuid.uuid1().hex
    # send to Behavior analyzer and time_pool
    send_q.put_nowait(data)
    debug(f'p: send_q.qsize() = {send_q.qsize()}')
    # sava data_list to local.
    # with open('../data/' + data['data_number'], 'w') as f:
    #     f.write(json.dumps(data_list))


# start
if __name__ == "__main__":
    try:
        asyncio.run(preprocessor())
    except KeyboardInterrupt:
        info('exit]')

