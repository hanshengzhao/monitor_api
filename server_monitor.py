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

from django.db import connections

def close_db(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        try:
            connections.close_all()
            # or do this
            # print(connections.close_all(), 'close_db')
        except Exception as e:
            print(e, 'close_db')
        return result
    return wrapper


@close_db
def judge_server(server):
    req_object = ReqInfo.objects.all()
    print "judge",server.server_name
    now_time = time.mktime(timezone.now().timetuple())
    last_alarm = server.last_alarm_date
    last_alarm = time.mktime(last_alarm.timetuple())
    if now_time - last_alarm < server.inspection_interval:
        return None
    server_id = server.server_id
    server_interval = server.inspection_interval
    req_obj = req_object.filter(server_id=server_id).order_by("-req_date")
    if req_obj.count() > 0:
        last_time = req_obj[0].req_date
        last_time = time.mktime(last_time.timetuple())
        if now_time - last_time <= int(server_interval):
            pass
        else:
            url = server.alarm.Alarm_url
            rec_user = server.alarm_user
            message = "%s id is %s is unreachable in %s s  %s" % (server.server_name, server.server_id, server_interval,ctime())
            send_alarm(url, rec_user, '%s unreachable' % server.server_name, message)
            # 添加一个未可达请求信息到请求数据里
            unreachable_req = ReqInfo()
            unreachable_req.req_user = server.req_user
            unreachable_req.server_id = server.server_id
            unreachable_req.server_name = server.server_name
            unreachable_req.alarm_user = server.alarm_user
            unreachable_req.alarm = server.alarm
            unreachable_req.server_status = "unreachable"
            unreachable_req.is_alarm = True
            unreachable_req.interval = server_interval
            unreachable_req.req_date = timezone.now()
            unreachable_req.other = "unreachable"
            unreachable_req.is_unreachable = True
            unreachable_req.save()
            server.last_alarm_date = timezone.now()
            server.save()



def monitor_daemon(pool):
    all_server = Server_Reg.objects.all()
    requests = threadpool.makeRequests(judge_server,all_server)
    [pool.putRequest(req) for req in requests]


pool = threadpool.ThreadPool(10)
while True:
    monitor_daemon(pool)
    pool.wait()


# server_id = 'login_server'
# obj1 = ReqInfo.objects
#
# while True:
#     last_obj = obj1.filter(server_id=server_id).order_by("-req_date")
#     print last_obj[0]
#     time.sleep(2)
#

# 删除未注册的
# from django.db.models import Q
# q1 = Q()
# q1.connector = "OR"
# all_server = Server_Reg.objects.all()
# for server  in all_server:
#     q1.children.append(('server_id',server.server_id))
# print  ReqInfo.objects.exclude(q1).delete()
    # ReqInfo.objects.exclude(server_id=server.server_id).delete()