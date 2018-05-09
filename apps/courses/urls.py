# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/4/2 17:45'
from django.conf.urls import url, include
from .views import CourseListView,CourseDetailView,CourseVideoView,CourseCommentView,AddCommentView,CoursePlayView


urlpatterns = [
    #课程列表页
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    #课程详情页
    url(r'^detail/(?P<course_id>.*)/$',CourseDetailView.as_view(),name='course_detail'),
    #课程章节页
    url(r'^video/(?P<course_id>.*)/$',CourseVideoView.as_view(),name='course_video'),
    #课程用户评论页
    url(r'^comment/(?P<course_id>.*)/$',CourseCommentView.as_view(),name='course_comment'),
    #课程视频播放页
    url(r'^play/(?P<video_id>.*)/$',CoursePlayView.as_view(),name='course_play'),

    #--------------用户收藏------------
    url(r'^add_comment/$',AddCommentView.as_view(),name='add_comment')
]