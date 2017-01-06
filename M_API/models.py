#! /usr/bin/env python
# -*- coding: utf-8

from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, UserManager
from django.utils import timezone
import datetime

PROJECT_ITEM = (
    ('DK', u'大卡'),
    ('HY', u'货运'),
    ('YY', u'运营'),
    ('YYZC', u'运营支撑'),
    ('ZY', u'智运'),

)



# IDC_ITEM = (
#     ('1',u'M6'),
#     ('2',u'世纪互联'),
# )


# 定义IDC信息
class IDCInfo(models.Model):
    IDC_name = models.CharField(max_length=48, verbose_name=u'idc机房')
    IDC_url = models.URLField(max_length=128, verbose_name=u'URL')

    def __unicode__(self):
        return u'%s' % self.IDC_name

    class Meta:
        verbose_name = u'IDC机房信息'
        verbose_name_plural = u'IDC机房信息'


# 定义用户信息
class UserInfo(User):
    project = models.CharField(choices=PROJECT_ITEM, max_length=48, verbose_name=u'项目名称')
    IDC = models.ForeignKey(IDCInfo)
    REQUIRED_FIELDS = ['project', 'IDC']
    objects = UserManager()

    def __unicode__(self):
        return u'%s' % self.username

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = u"用户信息"


# 定义报警方式
class AlarmInfo(models.Model):
    Alarm_name = models.CharField(max_length=48, verbose_name=u'报警名称')
    Alarm_url = models.CharField(max_length=48, verbose_name=u'触发地址')

    def __unicode__(self):
        return u'%s' % self.Alarm_name

    class Meta:
        verbose_name = u'报警方式'
        verbose_name_plural = u'报警方式'


# SERVER_STATUS = (
#     (-1,u'其他'),
#     (0,u'正常'),
#     (1,u'警告'),
#     (2,u'严重'),
# )

# 定义 请求数据记录信息
class ReqInfo(models.Model):
    req_user = models.ForeignKey(UserInfo, verbose_name=u'请求者')
    server_id = models.CharField(max_length=128, verbose_name=u'服务ID')
    server_name = models.CharField(max_length=128, verbose_name=u'服务名称')
    alarm_user = models.CharField(max_length=1024, verbose_name=u'报警对象')
    alarm = models.ForeignKey(AlarmInfo, verbose_name=u'报警方式')
    # server_status = models.IntegerField(choices=SERVER_STATUS,verbose_name=u'服务状态')
    server_status = models.CharField(max_length=512, verbose_name=u'服务状态')
    is_alarm = models.BooleanField(verbose_name=u'是否报警')
    interval = models.IntegerField(verbose_name=u'报警间隔')
    req_date = models.DateTimeField(verbose_name=u'请求时间')
    other = models.TextField(verbose_name=u'其他')
    is_unreachable = models.BooleanField(default=False,verbose_name=u'不可达请求')
    def __unicode__(self):
        return u"%s | %s | %s | 是否不可达 %s" % (self.server_name, self.server_id, self.req_date,self.is_unreachable)

    class Meta:
        verbose_name = u'请求数据'
        verbose_name_plural = u'请求数据'


# 注册要监控服务
class Server_Reg(models.Model):
    req_user = models.ForeignKey(UserInfo, verbose_name=u'请求者')
    server_id = models.CharField(max_length=128, verbose_name=u'服务ID')
    server_name = models.CharField(max_length=128, verbose_name=u'服务名称')
    inspection_interval = models.IntegerField(verbose_name=u'检测间隔')
    alarm = models.ForeignKey(AlarmInfo, verbose_name=u'报警方式')
    alarm_user = models.CharField(max_length=1024, verbose_name=u'报警对象')
    last_alarm_date = models.DateTimeField(verbose_name=u'上次未检测到的报警时间', default=datetime.datetime.now())

    def __unicode__(self):
        return self.server_name + self.server_id

    class Meta:
        verbose_name = u'监控服务注册'
        verbose_name_plural = u'监控服务注册'


# 统计请求情况
class Req_Statistics(models.Model):
    req_user = models.ForeignKey(UserInfo,verbose_name=u'请求者')
    normal_req_count = models.IntegerField(verbose_name=u'正常请求次数')
    alarm_req_count = models.IntegerField(verbose_name=u'报警请求次数')
    unreachable_req_count = models.IntegerField(verbose_name=u'不可达次数')
    server_id = models.CharField(max_length=128, verbose_name=u'服务ID')
    server_name = models.CharField(max_length=128,verbose_name=u'服务名称')

    def __unicode__(self):
        return  "%s | %s |%s | %s"%(self.server_id,self.normal_req_count,self.alarm_req_count,self.unreachable_req_count)

    class  Meta:
        verbose_name = u'请求次数统计'
        verbose_name_plural = u'请求次数统计'