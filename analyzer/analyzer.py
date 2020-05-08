#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import ssl
import json
import socket
import asyncio
sys.path.append('..')
import numpy as np
import pandas as pd
import tensorflow as tf
from config import HOST, PORT, MODEL_PATH
from log import info, success, debug, warning, error, err_exp 
from exception.handle import handle_exception
try:
    from main_model import prepare_data
except:
    from analyzer.main_model import prepare_data


model = None
LABELS = None
ca_q = None


async def recv_data(reader, writer):
    address = writer.get_extra_info('peername')
    info(f'a: connection accepted from {address}.')
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(handle_exception)
    while True:
        try:
            data = await reader.readuntil(b'}')
            data = json.loads(data)
            debug(f'a: len(data): {len(data)}')
            debug(f'a: data.keys(): {data.keys()}')
            if data:
                await predict_data(data)
            else:
                raise Exception('Data is None!')
                pass
            debug(f'a: data = {data}, tpye: {type(data)}')
            if data == b'exit}':
                info(f'a: message terminated, closing connection.')
                writer.close()
                return
        except ConnectionResetError as e:
            warning(f'a: {address}: Connection Reset Error!')
            return
        except asyncio.streams.IncompleteReadError as e:
            info(f"a: {address}: The customer's office has closed the connection.")
            writer.close()
            return

async def predict_data(data):
    global model, LABELS, ca_q
    if model and LABELS:
        values = []
        columns = sorted(data.keys())
        for i in columns:
            values.append(data.get(i))
        df = pd.DataFrame([values], columns=columns)
        no_uses = ['src', 'dst', 'sport', 'dport', 'time', 'data_number']
        for i in no_uses:
            df.pop(i)
        x = prepare_data(df)
        res = model.predict(x)
        data['label'] = LABELS[np.argmax(res, axis=1)[0]]
        if ca_q:
            ca_q.put_nowait(data)
        debug(f'a: predict_res = {res}, label = {data["label"]}')
    else:
        error(f'Model or Labels is None!')
        data['label'] = None


async def load_model():
    global model, LABELS
    info(f'a: loading the model and labels...')
    model = tf.keras.models.load_model('../' + MODEL_PATH + '.h5')
    with open('../' + MODEL_PATH + '.labels', 'r') as f:
        LABELS = json.loads(f.read())
    success(f'a: load model success.')


async def analyzer(host, port, q=None):
    global ca_q
    try:
        if not ca_q:
            ca_q = q
            info(f'a: set ca_q success.')
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain('../cert/cacert.pem', '../cert/privkey.pem', 'e3fb285c6276363050fc73b05ea7f0a1')
        await load_model()
        #d = {'protocol_type': 'TCP', 'urgent': 0, 'hot': 0, 'src_bytes': 140, 'dst_bytes': 2497, 'service': 'http', 'flag': 'SF', 'duration': 0, 'count': 0, 'srv_count': 0, 'serror_rate': 0, 'rerror_rate': 0, 'same_srv_rate': 0, 'diff_srv_rate': 0, 'srv_serror_rate': 0, 'srv_rerror_rate': 0, 'srv_diff_host_rate': 0, 'dst_host_count': 0, 'dst_host_srv_count': 0, 'dst_host_same_srv_rate': 0.0, 'dst_host_diff_srv_rate': 1.0, 'dst_host_same_src_port_rate': 0.0, 'dst_host_serror_rate': 0, 'dst_host_rerror_rate': 0, 'dst_host_srv_diff_host_rate': 0, 'dst_host_srv_serror_rate': 0, 'dst_host_srv_rerror_rate': 0}
        #await predict_data(d)
        server = await asyncio.start_server(recv_data, host, port, ssl=ssl_context)
        info(f'a: starting server on {host}:{port}')
        #while True:
        #    await server.start_serving()
        #    debug(f'aaa')
        await server.serve_forever()
    except Exception as e:
        error(f'a: {e}')
        err_exp(e)


if __name__ == '__main__':
    try:
        asyncio.run(analyzer(HOST, PORT))
    except KeyboardInterrupt as e:
        info('exit]')

