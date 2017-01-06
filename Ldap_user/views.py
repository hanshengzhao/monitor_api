#! coding:utf-8
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response, HttpResponse, render,redirect,resolve_url
from django.contrib.auth.decorators import login_required
# from api import login_ldap
# Create your views here.
#
def login_ldap(user,passwd):
    return True

# 判断用户是否登陆装饰器
def is_login(func,*args, **kwargs):

    def _deco(req,*args, **kwargs):
        if req.COOKIES.get('username', False):
            return func(req,*args, **kwargs)
        else:
            return render(req, "login.html", {'error': '请登录'})
    return _deco


def login(req):
    if req.method == "GET":
        return render(req,"login.html")
    else:
        username = req.POST.get('username')
        password = req.POST.get('password')
        if login_ldap(username,password):
            print "set cookie %s"%username
            response = redirect(resolve_url('project_chart'))
            response.set_cookie('username',username,expires=3600)
            return response
        else:
            return   render(req,"login.html",{'error':'认证失败'})


