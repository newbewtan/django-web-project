# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/27 16:29'
from django.conf.urls import url, include
from organization.views import OrgListView
from  .views import AddAskView,OrgDetailHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView

urlpatterns=[
    # -------  慕学课程机构首页 -----------
    url(r'^org_list/$', OrgListView.as_view(), name='org_list'),
    url(r'^add_ask/$',AddAskView.as_view(),name='add_ask'),
    url(r'detail_home/(?P<org_id>\d+)/$',OrgDetailHomeView.as_view(),name='detail_home'),
    url(r'org_courses/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name='org_course'),
    url(r'org_desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name='org_desc'),
    url(r'org_teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teacher'),
    # -------------用户收藏---------------------
    url(r'add_fav/$', AddFavView.as_view(), name='add_favo')

]