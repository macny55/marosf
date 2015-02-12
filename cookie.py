#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime

def set_cookie(self, data, expire):
    expires_date = datetime.datetime.utcnow() + datetime.timedelta(expire)
    expires_formatted = expires_date.strftime("%d %b %Y %H:%M:%S GMT")

    self.response.headers.add_header(
       'Set-Cookie', 
       'access_token=' + data + '; expires='+ expires_formatted + ';path=/;')

def set_cookie_usr_name(self, data, expire):
    expires_date = datetime.datetime.utcnow() + datetime.timedelta(expire)
    expires_formatted = expires_date.strftime("%d %b %Y %H:%M:%S GMT")

    self.response.headers.add_header(
       'Set-Cookie', 
       'usr_name=' + data + '; expires='+ expires_formatted + ';path=/;')

def load_cookie_usr_name(self):
    return self.request.cookies.get('usr_name', '')

def load_cookie(self):
    return self.request.cookies.get('access_token', '')

def del_cookie(self):
    set_cookie(self, "deleted", 10)
    set_cookie_usr_name(self, "deleted", 10)
