#!/usr/bin/env python3
# -*- author:xuanGe -*-
# -*- coding:utf-8 -*-
# -*- date:2020-2-14 -*-
import sys
from log import info, success, debug, warning, error, err_exp


def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    if context.get('message') == 'Fatal error on SSL transport':
        return
    error(context)
    err_exp(context.get('exception'))
    error(f"Caught exception: {msg}")
