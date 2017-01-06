#!/bin/env python
# -*- coding:utf-8 -*-
# created by hansz
from django import forms
from models import *

class user_form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(user_form,self).__init__(*args,**kwargs)

    class Meta :
        model = UserInfo
        fields = ['username','password','project','IDC','email']