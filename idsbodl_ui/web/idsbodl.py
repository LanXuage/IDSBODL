#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import asyncio
import threading
import subprocess


class Idsbodl(threading.Thread):
    def __init__(self):
        pass


    @classmethod
    def get_collectors(cls):
        ret = subprocess.check_output(['fdfs_monitor', '/etc/fdfs/client.conf'])
        m = re.findall(b'ip_addr = (.*?) ', ret)
        return m

    
    def run(self):
        


if __name__ == '__main__':
    Idsbodl().get_collectors()
