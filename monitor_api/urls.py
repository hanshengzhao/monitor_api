"""monitor_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
# from rest_framework import routers
from M_API import views
from Ldap_user import views as ldap_views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^register', views.register,name='register'),

    url(r'^monitor', views.monitor,name='monitor'),
    url(r'^delete', views.del_reg_server,name='del_reg_server'),
    url(r'^req_info', views.req_info,name='req_info'),
    url(r'^chart$', views.monitor_info,name='project_chart'),
    url(r'^chart/(?P<PROJECT>\w*)', views.server_monitor_info,name='server_monitor_info'),

    url(r'^login', ldap_views.login, name='login'),
    url(r'^', ldap_views.login, name='login_'),

    # url(r'^', views.register,name='register'),

    # url(r'^', include(router.urls)),

    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
