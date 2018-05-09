# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/4/11 10:12'

from django.conf.urls import url,include
from .views import TeacherListView,TeacherDetailView
urlpatterns=[
    url(r'^teacher/$',TeacherListView.as_view(),name='teacher'),
    url(r'^detail/(?P<teacher_id>.*)$',TeacherDetailView.as_view(),name='detail')
]