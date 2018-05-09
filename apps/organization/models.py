from  datetime import datetime

from django.db import models

#------------机构城市-----------------------------------
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200,verbose_name='城市描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#------课程机构---------
class CourseOrg(models.Model):
    name = models.CharField(max_length=50,verbose_name='机构名称')
    category=models.CharField(default='pxjg',max_length=20,choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')),verbose_name='机构类别')
    desc = models.TextField(verbose_name='机构描述')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')

    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面图', max_length=100)

    address = models.CharField(max_length=150,verbose_name='机构地址')
    city = models.ForeignKey(CityDict,verbose_name='所在城市')
    students=models.IntegerField(default=0,verbose_name='学习人数')
    course_nums=models.IntegerField(default=0,verbose_name='课程数')
    add_time = models.DateTimeField(default=datetime.now)

    # teachers=

    class Meta:
        verbose_name='课程机构'
        verbose_name_plural=verbose_name
    def get_teacher_number(self):
        return  self.teachers_set.all().count()
        #相当于 courseOrg.teacher_set.all().count()，获取到机构内所有的教师数
    def get_course_nums(self):
        return self.course_set.all().count()


    def __str__(self):
        return  self.name



#------------机构教师------------------
class Teachers(models.Model):

    org=models.ForeignKey(CourseOrg,verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名')
    work_years = models.IntegerField(default=0,verbose_name='工作年限')
    work_company = models.CharField(max_length=50,verbose_name='就职公司')
    work_position = models.CharField(max_length=50,verbose_name='公司职位')
    point = models.CharField(max_length=50,verbose_name='教学特点')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')
    age=models.IntegerField(default=0,verbose_name='年龄')
    char=models.TextField(default='',verbose_name='教师简介',max_length=200)

    images = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='教师头像', max_length=100,null=True,blank=True)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
