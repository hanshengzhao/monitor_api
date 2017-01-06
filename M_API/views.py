#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
###
from django.contrib.auth.models import User, Group
# from rest_framework import viewsets
# from serializers import UserSerializer, GroupSerializer
from django.shortcuts import render_to_response, HttpResponse, render
from  api import *
import models, forms
import json
from django.utils import timezone
from Ldap_user.views import is_login


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     允许查看和编辑user 的 API endpoint
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     允许查看和编辑group的 API endpoint
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

@is_login
def register(req):
    if req.method == 'GET':
        project_info = models.PROJECT_ITEM
        IDC_info = models.IDCInfo.objects.all()
        return render_to_response('register.html', locals())
    else:
        # user_info = forms.user_form(req.POST)
        # print user_info
        username = req.POST.get('username')
        password = req.POST.get('password')
        email = req.POST.get('email')
        project = req.POST.get('project')
        is_user = get_object(models.UserInfo, username=username)
        if is_user:
            return render_to_response('register.html', {'error': "用户名已存在"})
        else:
            user_info = forms.user_form(req.POST)
            print user_info
            user_info.save()
            message = u'''
                您好:
                    您注册的api的用户名是 %s\n;
                    密码是 %s\n;
                    所属的项目组是 %s\n ;
            ''' % (username, password, project)
            # send_message([email],u'用户注册信息',message)
            try:
                send_url = get_object(models.AlarmInfo, Alarm_name='mail').Alarm_url
            except Exception as e:
                send_url = "http://58.83.210.31:8866/mail_sms/mail.php"
            send_alarm(send_url, email, u'用户注册信息', message)
            print '%s register project is %s ' % (username, project)
            return HttpResponse(u'请注意查收注册邮件,如未收到请联系系统支持部')


req_format = {
    "username": "huoyun",
    "is_alarm": True,
    "server_name": "apache",
    "server_id": "aaaaaaaaaaaaaaaaaaaaaa",
    "interval": 30,
    "server_status": "Unknow Error",
    "alarm_user": "hanshengzhao@vip.qq.com;403643245@qq.com",
    "other": "请按照此格式请求",
    "password": "huoyun",
    "alarm_type": "wechat"
}

response_format = {
    'status': '',
    'code': '',
    'text': '',
}
delete_format = {
    'username': 'huoyun',
    'password': 'huoyun',
    'server_id': 'aaaaaaaaaaaaaaaaaaaaaa'
}


# 定义监控请求
def monitor(req):
    if req.method == "GET":
        # print  'monitor get request'
        username = req.GET.get('username', None)
        if username:
            server_list = models.Server_Reg.objects.filter(req_user__username=username)
            ret_list = []
            for server in server_list:
                server_info = {
                    'server_id': server.server_id,
                    'server_name': server.server_name,
                    'inspection_interval': server.inspection_interval,
                    'alarm_user': server.alarm_user,
                    'alarm': server.alarm.Alarm_name,
                    'last_alarm_date': str(server.last_alarm_date),
                }
                ret_list.append(server_info)
            server_infos = json.dumps(ret_list)
        else:
            ret_list = {'message': 'Please provide username'}
            server_infos = json.dumps(ret_list)
        return HttpResponse(server_infos, content_type="application/json")


    elif req.method == "DELETE":
        print req.method
        return delete_reg_server(req)
    else:
        print req.method
        print  'monitor post request'
        res = response_format
        try:
            data = json.loads(req.body)
            username = data['username']
            password = data['password']
            user_info = get_object(models.UserInfo, username=username, password=password)
            if not user_info:
                res['status'] = False
                res['code'] = 401
                res['text'] = 'Auth Failed'
            else:
                # 判断其他参数是否合法
                server_name = data['server_name']
                server_id = data['server_id']
                inspection_interval = data['interval']
                alarm_name = data['alarm_type']
                # alarm_obj = models.AlarmInfo.objects.filter(Alarm_name=alarm_name)
                alarm_obj = get_object(models.AlarmInfo, Alarm_name=alarm_name)
                if not alarm_obj:
                    raise TypeError
                # if len(alarm_obj) <= 0:
                #     raise TypeError
                alarm_user = data['alarm_user']
                is_alarm = data['is_alarm']
                server_status = data['server_status']
                other = data['other']
                # 判断server id 是否已经存在,不存在的话去加入轮询去判断
                req_obj = models.Server_Reg.objects.filter(server_id=data['server_id'])
                if len(req_obj) <= 0:
                    # 注册服务
                    print  "reg server %s,id is %s" % (server_name, server_id)
                    server_reg = models.Server_Reg()
                    server_reg.req_user = user_info
                    server_reg.server_name = server_name
                    server_reg.server_id = server_id
                    server_reg.inspection_interval = inspection_interval
                    server_reg.alarm = alarm_obj
                    server_reg.alarm_user = alarm_user
                    server_reg.save()
                    send_alarm(alarm_obj.Alarm_url, user_info.email, u'注册监控服务',
                               u'您已成功注册监控服务,%s, id 是 %s' % (server_name, server_id))
                monitor_req_info = models.ReqInfo()
                monitor_req_info.server_id = server_id
                monitor_req_info.server_name = server_name
                monitor_req_info.req_user = user_info
                monitor_req_info.is_alarm = is_alarm
                monitor_req_info.alarm = alarm_obj
                monitor_req_info.server_status = server_status
                monitor_req_info.interval = inspection_interval
                monitor_req_info.alarm_user = alarm_user
                monitor_req_info.req_date = timezone.now()
                monitor_req_info.other = other
                monitor_req_info.save()
                if data['is_alarm']:
                    print u"发送报警信息给", alarm_user.split(';')
                    print monitor_req_info.alarm.Alarm_url
                    send_alarm(monitor_req_info.alarm.Alarm_url, alarm_user, u'%s 报警' % server_name,
                               u'%s status is %s ,other info is %s' % (server_name, server_status, other))
                    res['text'] = 'Alerm Ok'
                else:
                    res['text'] = 'Send Ok'
                res['status'] = True
                res['code'] = 200
        except TypeError:
            res['status'] = False
            res['code'] = 400
            res['text'] = 'arguments error ,alarm type not exists.'
        except Exception as e:
            print e
            res['status'] = False
            res['code'] = 400
            res['text'] = 'arguments error %s' % e
        return HttpResponse(json.dumps(res))


def delete_reg_server(req):
    data = json.loads(req.body)
    username = data['username']
    password = data['password']
    # print username,password
    res = {}
    if username and password:
        user_obj = get_object(models.UserInfo, username=username, password=password)
        if user_obj:
            server_id = data['server_id']
            try:
                server_obj = get_object(models.Server_Reg, server_id=server_id, req_user=user_obj)
                if not server_obj:
                    raise TypeError
                # models.Server_Reg.objects.get(server_id=server_id).delete()
                server_obj.delete()
                print '%s delete server %s ' % (username, server_id)
                try:
                    send_url = get_object(models.AlarmInfo, Alarm_name='mail').Alarm_url
                except Exception as e:
                    send_url = "http://58.83.210.31:8866/mail_sms/mail.php"
                send_alarm(send_url, user_obj.email, u'删除服务%s' % (server_id), u'已删除监控服务%s' % (server_id))
                res['status'] = True
                res['code'] = 200
                res['text'] = 'Delete Success'
            except:
                res['status'] = False
                res['code'] = 404
                res['text'] = 'Server id not found'
        else:
            res['status'] = False
            res['code'] = 401
            res['text'] = 'Auth failed'
    else:
        res['status'] = False
        res['code'] = 401
        res['text'] = 'you must post username and passowrd'
    return HttpResponse(json.dumps(res))


def del_reg_server(req):
    if req.method == "POST":
        data = json.loads(req.body)
        username = data['username']
        password = data['password']
        # print username,password
        res = {}
        if username and password:
            user_obj = get_object(models.UserInfo, username=username, password=password)
            if user_obj:
                server_id = data['server_id']
                try:
                    get_object(models.Server_Reg, server_id=server_id)
                    models.Server_Reg.objects.get(server_id=server_id).delete()
                    print '%s delete server %s ' % (username, server_id)
                    try:
                        send_url = get_object(models.AlarmInfo, Alarm_name='mail').Alarm_url
                    except Exception as e:
                        send_url = "http://58.83.210.31:8866/mail_sms/mail.php"
                    send_alarm(send_url, user_obj.email, u'删除服务%s' % (server_id), u'已删除监控服务%s' % (server_id))
                    res['status'] = True
                    res['code'] = 200
                    res['text'] = 'Delete Success'
                except:
                    res['status'] = False
                    res['code'] = 404
                    res['text'] = 'Server id not found'
            else:
                res['status'] = False
                res['code'] = 401
                res['text'] = 'Auth failed'
        else:
            res['status'] = False
            res['code'] = 401
            res['text'] = 'you must post username and passowrd'
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponse(json.dumps(delete_format))





# 所有请求记录
def req_info(req):
    if req.method == "GET":
        req_info = models.ReqInfo.objects.all()
        all_req_list, p, req_lists, page_range, current_page, show_first, show_end = pages(req_info, req)
        return render_to_response('req_info.html', locals())


# 监测所有Server_Req里面的服务是否按时间间隔发送请求
import datetime


# 所有项目监控情况
@is_login
def monitor_info(req):
    if req.method == "GET":
        # 最近半个小时各个项目的请求
        PROJECT_ITEM = models.PROJECT_ITEM

        # 报警个数
        req_date = timezone.now() - datetime.timedelta(minutes=30)
        print req_date, timezone.now()
        datas = []
        for value, name in PROJECT_ITEM:
            alarm_count = models.ReqInfo.objects.filter(req_date__gte=req_date, req_user__project=value, is_alarm=True,
                                                        is_unreachable=False).count()
            # 未报警的请求个数
            normal_count = models.ReqInfo.objects.filter(req_date__gte=req_date, req_user__project=value,
                                                         is_alarm=False,
                                                         is_unreachable=False).count()
            # 不可达个数 注册服务最近半个小时的应请求数  减去 总请求数，就是缺少的请求数
            unreachable_count = models.ReqInfo.objects.filter(req_date__gte=req_date, req_user__project=value,
                                                              is_unreachable=True).count()
            data = {'project': name, 'project_id': value, 'alarm_count': alarm_count, 'normal_count': normal_count,
                    'unreachable_count': unreachable_count}
            datas.append(data)
        print datas
        return render_to_response('project_chart.html', {'datas': datas})


@is_login
def server_monitor_info(req, PROJECT):
    if req.method == "GET":
        # 最近半个小时各个服务的请求
        project_name = False
        for project in models.PROJECT_ITEM:
            if PROJECT in project:
                project_name = project[1]
        if not project_name:
            return HttpResponse(u'没有此项目')

        # 报警个数
        req_date = timezone.now() - datetime.timedelta(minutes=30)
        print req_date, timezone.now()
        datas = []
        # 获取所有的服务
        # all_server =  models.ReqInfo.objects.filter(req_user__project=PROJECT).values('server_id').distinct()
        all_server = models.Server_Reg.objects.filter(req_user__project=PROJECT).values('server_id').distinct()
        print all_server
        for server in all_server:
            server_id = server['server_id']
            # print "filter ret ",models.ReqInfo.objects.filter(server_id=server_id)[0]
            servre_name = models.ReqInfo.objects.filter(server_id=server_id)[0].server_name
            alarm_count = models.ReqInfo.objects.filter(server_id=server_id, req_date__gte=req_date,
                                                        req_user__project=PROJECT, is_alarm=True,
                                                        is_unreachable=False).count()
            # 未报警的请求个数
            normal_count = models.ReqInfo.objects.filter(server_id=server_id, req_date__gte=req_date,
                                                         req_user__project=PROJECT, is_alarm=False,
                                                         is_unreachable=False).count()
            # 不可达个数 注册服务最近半个小时的应请求数  减去 总请求数，就是缺少的请求数
            unreachable_count = models.ReqInfo.objects.filter(server_id=server_id, req_date__gte=req_date,
                                                              req_user__project=PROJECT, is_unreachable=True).count()
            data = {'project': servre_name + "%s" % server_id, 'alarm_count': alarm_count, 'normal_count': normal_count,
                    'unreachable_count': unreachable_count}
            datas.append(data)
        # print datas
        return render_to_response('server_chart.html', {'datas': datas, 'project_name': project_name, })
