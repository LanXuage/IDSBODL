#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import ssl
import json
import socket
import asyncio
import numpy as np
import pandas as pd
import tensorflow as tf
from config import HOST, PORT, MODEL_PATH
from log import info, success, debug, warning, error, err_exp 
from handle import handle_exception
from main_model import prepare_data


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
            if data:
                await predict_data(data)
            else:
                raise Exception('Data is None!')
                pass
            if data == b'exit}':
                info(f'a: message terminated, closing connection.')
                writer.close()
                return
        except ConnectionResetError as e:
            warnin/(f'a: {address}: Connection Reset Error!')
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
        debug(f'a: label = {data["label"]}')
    else:
        error(f'Model or Labels is None!')
        data['label'] = None


async def load_model():
    global model, LABELS
    info(f'a: loading the model and labels...')
    model = tf.keras.models.load_model(MODEL_PATH + '.h5')
    with open(MODEL_PATH + '.labels', 'r') as f:
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
        server = await asyncio.start_server(recv_data, host, port, ssl=ssl_context)
        info(f'a: starting server on {host}:{port}')
        # while True:
        #     await server.start_serving()
        #     debug(f'aaa')
        await server.serve_forever()
    except Exception as e:
        error(f'a: {e}')
        err_exp(e)


if __name__ == '__main__':
    try:
        asyncio.run(analyzer(HOST, PORT))
    except KeyboardInterrupt as e:
        info('exit]')

