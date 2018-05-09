from  __future__ import unicode_literals
from  datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teachers


class Course(models.Model):

    teacher=models.ForeignKey(Teachers,verbose_name='授课讲师',blank=True,null=True)
    id=models.IntegerField(primary_key=True,auto_created=True,verbose_name='课程ID',blank=True)


    categroy=models.CharField(max_length=20,verbose_name='课程类别',default='web前端/后端',null=False)

    course_org=models.ForeignKey(CourseOrg,verbose_name='所属机构',null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name='课程名称')
    desc = models.CharField(max_length=200,verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')#后期可能修改为富文本支持的
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2,verbose_name='难度')
    #choice 方法里面每个选项包括('value','dis_play')两个属性
    #例：实例化 a=Course(degree='cj')
    #         a.degree--->'cj'    a.get_degree_display()--->'初级'

    learn_times = models.IntegerField(default=0,verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name='封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    class_nums=models.IntegerField(default=0,verbose_name='课时数')
    notice=models.CharField(default='暂无',max_length=50,verbose_name='课程须知')
    knowledge=models.CharField(default='暂无',max_length=50,verbose_name='老师告诉你能学什么')
    course_res = models.FileField(upload_to='courses/course_res/%Y/%m', verbose_name='课程资源',null=True,blank=True)



    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')



    class Meta:
        verbose_name ='课程'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Lesson(models.Model):
    course=models.ForeignKey(Course,verbose_name='课程')
    #ForeignKey(),第一个参数传递一个关联的model的实例，也可以是未定义model的名称'*str'，还可以是本身'self'
    name=models.CharField(max_length=100,verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name='章节'
        verbose_name_plural=verbose_name

    def __str__(self):
        return  self.name


class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name='章节名称')
    name = models.CharField(max_length=100, verbose_name='视频名')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name='视频'
        verbose_name_plural=verbose_name
    def __str__(self):
        return  self.name


class CourseResource(models.Model):
    course=models.ForeignKey(Course,verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='资源名称')
    download=models.FileField(upload_to='course/resource/%Y/%m',verbose_name='资源文件',max_length=100)
    # todo upload_to 仅代表着上传的目标地址，而download才是存储数据文件的字段，或者说才是数据的索引
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name='课程资源'
        verbose_name_plural=verbose_name

    def __str__(self):
        return  self.name

