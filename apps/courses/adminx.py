# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/22 18:07'

from .models import  Course,Lesson,Video,CourseResource
import xadmin


class CourseAdmin(object):
    list_display = ['id','name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['id','name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['id','name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']
    #course__name 两个下划线指定 搜索对应外键的字段 不指定'__'将无法搜索


class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson__name','name','add_time']


class CourseResourceAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)