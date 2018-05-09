from  __future__ import unicode_literals
from  datetime import datetime

from django.db import models
from django.contrib.auth.models import  AbstractUser
from courses.models import Course
'''
用户模块:
    1.UserProfile--用户信息(继承自djangp官方的用户模型，拥有官方默认user模型字段，还可以按需求自定义添加字段)
        昵称  生日  性别  地址  手机号码  上传图片
    2.EmailVerifyRecord--邮箱验证码(用户注册/登陆是发送的验证请求所对应服务器返回的验证码,独立于课程和管理)
        验证码  邮箱地址  发送方式(注册/找回)   发送时间
    3.Banner--首页轮播图(网站首页轮播图，独立)
        标题  轮播图片  访问地址  轮播顺序  添加时间
'''


class UserProfile(AbstractUser):

    course= models.ForeignKey(Course,default='',max_length=20,verbose_name='参与课程')
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='')
    birday = models.DateField(verbose_name='生日',null=True,blank=True)
    gender = models.CharField(choices=(('male','男'),('female','女')),default='male',max_length=6,verbose_name='性别')
    address = models.CharField(max_length=100,default='',verbose_name='住址')
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name='手机号码')

    #upload_to方法获取image路径，方法内置了strftime()，能解析 %格式化日期
    image=models.ImageField(upload_to='use_image/%Y/%m',default='image/default.png',max_length=100,verbose_name='头像',blank=True,null=True)

    class Meta:

        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    #获取用户未读数量的方法
    def getUnreadMessage(self):
        from  operation.models import Usermessage
        return  Usermessage.objects.filter(user=self.id).count()

    # __unicode__()方法是在一个对象上调用unicode()时被调用的。因为Django的数据库后端会返回Unicode字符串给model属性，
    # 所以我们通常会给自己的model写一个__unicode__()方法,username 是django默认user模型的字段
    def __unicode__(self):
        return  self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name='验证码')
    email = models.EmailField(max_length=50,verbose_name='邮箱')
    send_type = models.CharField(choices=(('register','注册'),('forget','找回'),('update_email','修改邮箱')),max_length=15,verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')
    #将datetime.now()函数的括号去掉，目的是为了使返回值为类实例化的时间
    #带有括号的datetime.now()函数返回的是model 类编译的时间

    class Meta:
        verbose_name = '邮箱验证码' #代表model的名称，在后台显示
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return  '{0}({1})'.format(self.code,self.email)


class Banner(models.Model):#轮播图
    title = models.CharField(max_length=100,verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y%m',verbose_name='轮播图')
    url = models.URLField(max_length=200,verbose_name='访问地址')
    index = models.IntegerField(default=100,verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name




