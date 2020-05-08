#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import asyncio
import datetime
sys.path.append('..')
from config import ALARM_WHITE_LIST, DB_SESSION
from alarm_manager import send_alarm
from bases import Nids_data, Nids_protocol_type, Nids_service, Nids_flag, Nids_label
from log import debug, info, error


async def controller(q=None):
    info(f'ctrler: starting controller.')
    if not q:
        error(f'ctrler: q is None')
        return
    db_session = DB_SESSION()
    while True:
        try:
            data = await q.get()
            label = data.get('label')
            if label:
                if label not in ALARM_WHITE_LIST:
                    await send_alarm(data)
                # insert db
                error(f'{data["time"]}--type{type(data["time"])}')
                data['time'] = datetime.datetime.fromtimestamp(data['time'])
                error(Nids_data(**data).to_dict())
                #db_session.add()
                #db_session.commit()
        except Exception as e:
            error(e)
            pass


if __name__ == '__main__':
    try:
        asyncio.run(controller())
    except KeyboardInterrupt as e:
        info('exit]')

