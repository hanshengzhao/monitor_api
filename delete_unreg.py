#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz

import time,datetime
import os, sys,django
from django.utils import timezone
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["DJANGO_SETTINGS_MODULE"]="monitor_api.settings"
django.setup()
from M_API.models import Server_Reg,ReqInfo
from M_API.api import send_alarm
import threading
from time import ctime,sleep
import threadpool


def delete_unreg():
    from django.db.models import Q
    q1 = Q()
    q1.connector = "OR"
    all_server = Server_Reg.objects.all()
    for server  in all_server:
        q1.children.append(('server_id',server.server_id))
    print  ReqInfo.objects.exclude(q1).delete()


delete_unreg()
