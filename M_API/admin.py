from django.contrib import admin
from models import *
# Register your models here.
from django.contrib import admin

admin.site.register(UserInfo)
admin.site.register(IDCInfo)
admin.site.register(AlarmInfo)
admin.site.register(ReqInfo)
admin.site.register(Server_Reg)
admin.site.register(Req_Statistics)