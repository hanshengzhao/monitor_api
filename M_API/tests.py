from django.test import TestCase

# Create your tests here.

import requests
data = {
    'username': 'huoyun',
    'alarm_type': 'mail',
    'server_id': 'gfgdsgfdsggdf',
    'other': 'fffff',
    'server_name': 'nginx process',
    'is_alarm': True,
    'password': 'huoyun',
    'alarm_user': 'hanshengzhao@sinoiov.com',
    'interval': 120,
    'server_status': 'Unknow Error'
}
# data = {
#     'username': 'huoyun',
#     'server_id': 'bbbgfgdfsgsd',
#     'password': 'huoyun',
# }
import json
import uuid


# a = uuid.uuid4()
# import pdb
#
# pdb.set_trace()

def req_monitor(data):
    # ret = requests.post('http://172.90.4.55:8888/monitor', data=data, headers={'Content-Type': 'application/json'})
    data = json.dumps(data)
    print data
    ret = requests.post('http://localhost:8000/monitor', data=data, headers={'Content-Type': 'application/json'})
    print ret.content


data_list = []
for i in range(100):
    data = {
        'username': 'huoyun',
        'alarm_type': 'mail',
        'server_id': 'test %s' % i,
        'other': 'test',
        'server_name': 'test %s' % i,
        'is_alarm': False,
        'password': 'huoyun',
        'alarm_user': 'hanshengzhao@sinoiov.com',
        'interval': 120,
        'server_status': 'Unknow Error'
    }
    data_list.append(data)

print data_list
import threadpool
while True:
    pool=threadpool.ThreadPool(100)
    reqs =threadpool.makeRequests(req_monitor,data_list)
    [pool.putRequest(req)for req in reqs]
    pool.wait()



