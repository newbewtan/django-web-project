# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/22 17:00'
import  xadmin

from .models import  EmailVerifyRecord,Banner

#  -----------  Models of Users------------------------
class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type']
    list_filter=['code','email','send_type','send_time']


class BennerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BennerAdmin)
