# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/27 16:38'
from django.conf.urls import url,include
from  .views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView,ModifyPwdView,LogoutView

urlpatterns=[
    # -----  用户中心 --------
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register'),

    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='pwd_reset'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

]

#全局404函数定义
