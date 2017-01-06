#! coding:utf-8
from django.test import TestCase

import os
import sys
import ldap


def login_ldap(username, password):
    try:
        print("开始执行")
        conn = ldap.initialize(LDAP_SERVER)
        conn.set_option(ldap.OPT_REFERRALS, 0)
        conn.protocol_version = ldap.VERSION3

        # conn.simple_bind(username, password)
        conn.simple_bind_s('uid=%s,ou=People,dc=trafficguide,dc=com,dc=cn' % username, password)
        print '认证成功'
        return True
    except ldap.LDAPError, e:
        print("认证失败")
        print e
        return False


if __name__ == "__main__":
    LDAP_SERVER = "ldap://ldap-m6.ops.trafficguide.com.cn:389"
    username = "hanshengzhao"
    password = ""
    login_ldap(username, password)
else:
    from django.conf import settings

    LDAP_SERVER = settings.LDAP_SERVER
