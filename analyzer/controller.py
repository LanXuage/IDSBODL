#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-13 -*-
import sys
import asyncio
import datetime
from config import ALARM_WHITE_LIST, DB_SESSION
from alarm_manager import send_alarm
from bases import Nids_data, Nids_protocol_type, Nids_service, Nids_flag, Nids_label
from log import debug, info, error


async def controller(q=None):
    info(f'ctrler: starting controller.')
    if not q:
        error(f'ctrler: q is None')
        return
    db_sess = DB_SESSION()
    while True:
        try:
            data = await q.get()
            label = data.get('label')
            if label:
                if label not in ALARM_WHITE_LIST:
                    await send_alarm(data)
                # insert db
                info(data)
                data['time'] = datetime.datetime.fromtimestamp(data['time'])
                nids_data = Nids_data(**data)
                tmp = db_sess.query(Nids_protocol_type.id).filter(Nids_protocol_type.protocol_name==data.get('protocol_type')).first()
                if tmp:
                    nids_data.fk_nids_protocol_type_id = tmp[0]
                else:
                    raise Exception(f'Not "{data.get("protocol_type")}" protocol type in databases. ')
                tmp = db_sess.query(Nids_service.id).filter(Nids_service.service_name==data.get('service')).first()
                if tmp:
                    nids_data.fk_nids_service_id = tmp[0]
                else:
                    raise Exception(f'Not "{data.get("service")}" protocol type in databases. ')
                tmp = db_sess.query(Nids_flag.id).filter(Nids_flag.flag_name==data.get('flag')).first()
                if tmp:
                    nids_data.fk_nids_flag_id = tmp[0]
                else:
                    raise Exception(f'Not "{data.get("flag")}" protocol type in databases. ')
                tmp = db_sess.query(Nids_label.id).filter(Nids_label.label_name==data.get('label')).first()
                if tmp:
                    nids_data.fk_nids_label_id = tmp[0]
                else:
                    raise Exception(f'Not "{data.get("label")}" protocol type in databases. ')
                error(nids_data.to_dict())
                db_sess.add(nids_data)
                db_sess.commit()
        except Exception as e:
            error(e)
            db_sess.close()
            return


if __name__ == '__main__':
    try:
        asyncio.run(controller())
    except KeyboardInterrupt as e:
        info('exit]')

