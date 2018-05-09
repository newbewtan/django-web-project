# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/22 20:19'
from .models import  *
import xadmin


class CityDictAdmin(object):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='城市描述')
    add_time = models.DateTimeField(default=datetime.now)

    list_display = ['name','desc','add_time']
    search_fields = ['name','desc','add_time']
    list_filter = ['name','desc','add_time']


class CourseOrgAdmin(object):
    list_display = ['name','desc','click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name','desc','click_nums','fav_nums','image','address','city']
    list_filter = ['name','desc','click_nums','fav_nums','image','address','city','add_time']


class TeachersAdmin(object):
    list_display = [ 'name','org', 'work_years', 'point', 'click_nums', 'fav_nums', 'add_time']
    search_fields = [ 'name','org', 'work_years', 'point', 'click_nums', 'fav_nums']
    list_filter = ['name','org',  'work_years', 'point', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teachers,TeachersAdmin )
xadmin.site.register(CourseOrg,CourseOrgAdmin)