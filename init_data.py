#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
import time, datetime
import os, sys, django
from django.utils import timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["DJANGO_SETTINGS_MODULE"] = "monitor_api.settings"
django.setup()

from M_API.models import IDCInfo, AlarmInfo

Idc_list = [
    {
        'IDC_name': 'M6',
        'IDC_url': 'http://170.90.4.54:8888',
    },

]

Alarm_list = [
    {
        'Alarm_name': 'sms',
        'Alarm_url': 'http://58.83.210.31:8866/mail_sms/sms.php',
    },

    {
        'Alarm_name': 'mail',
        'Alarm_url': 'http://58.83.210.31:8866/mail_sms/mail.php',
    },

    {
        'Alarm_name': 'wechat',
        'Alarm_url': 'http://58.83.210.31:8866/mail_sms/mail.php',
    },
]
for idc in Idc_list:
    if IDCInfo.objects.filter(IDC_name=idc['IDC_name']).count() == 0:
        idc_obj = IDCInfo()
        idc_obj.IDC_name = idc['IDC_name']
        idc_obj.IDC_url = idc['IDC_url']
        idc_obj.save()
        print " %s save succeed." % (idc['IDC_name'])
    else:
        print " %s has already exists." % (idc['IDC_name'])

for alarm in Alarm_list:
    if AlarmInfo.objects.filter(Alarm_name=alarm['Alarm_name']).count() == 0:
        alarm_obj = AlarmInfo()
        alarm_obj.Alarm_name = alarm['Alarm_name']
        alarm_obj.Alarm_url = alarm['Alarm_url']
        alarm_obj.save()
        print " %s save succeed." % (alarm['Alarm_name'])
    else:
        print " %s has already exists." % (alarm['Alarm_name'])
