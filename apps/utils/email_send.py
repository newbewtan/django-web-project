# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/25 11:17'
from random import Random
import random
from  django.core.mail import  send_mail
from mxonline.settings import EMAIL_FROM


from  users.models import  EmailVerifyRecord


def send_register_email(email,send_type='register'): #发送注册激活到邮箱

    email_record=EmailVerifyRecord()  #创建验证吗对象实例
    if send_type == 'update_email':
        random_str = generate_random_str(4)
    else:
        random_str=generate_random_str(16) #生成16位验证码
    email_record.code=random_str #将字符串赋值url
    email_record.email= email #将email 传递
    email_record.send_type=send_type
    email_record.save() #保存传递给数据库后台

    email_title=""
    email_body= ""

    if send_type == "register":
        email_title= "慕学在线网注册激活链接"
        email_body = "请点击下面的连接激活你的账号: http://127.0.0.1:8000/active/{0}".format(random_str)
        send_status=send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            return True
        else:
            return False


    elif send_type == 'forget':
        email_title = "慕学在线网密码重置链接"
        email_body = "请点击下面的连接激活你的账号: http://127.0.0.1:8000/reset/{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False
    elif send_type == 'update_email':
        email_title = "慕学在线网邮箱重新绑定"
        email_body = "你的邮箱验证码是:{0}".format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False
def  generate_random_str(randomlength=8):
    str=''
    char='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789'
    lenth=len(char)-1
    for i in range(randomlength):
        str+=char[random.randint(0,lenth)]
    return str