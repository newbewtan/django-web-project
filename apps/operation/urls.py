# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/4/11 16:09'

from  .views import IndexView,UserCenterView,UserAlterView,UserImageView,UserPassWdView,RstEmailView,SendEmailCodeView
from django.conf.urls import url, include

urlpatterns = [
    #-----------------首页索引-------------------------
    url(r'^$',IndexView.as_view(),name='index'),

    #-------------------用户中心块-------------------------
    url(r'^user_center/(?P<user_id>.*)',UserCenterView.as_view(),name='user_center'),
    #基础信息修改
    url(r'^user_alter',UserAlterView.as_view(),name='user_alter'),
    #用户头像修改
    url(r'^rst_head',UserImageView.as_view(),name='user_image'),
    #用户密码修改
    url(r'^rst_passwd',UserPassWdView.as_view(),name='user_passwd'),
    #发送邮箱验证码
    url(r'^sendemail_code',SendEmailCodeView.as_view(),name='sendemail_code'),
    #验证码重新绑定邮箱
    url(r'^rst_email',RstEmailView.as_view(),name='rst_email'),


]