# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/23 15:14'
from  django import  forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form): #form用于对后台提交的数据进行检测
    username=forms.CharField(required=True,min_length=5)
    password=forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form): #register 表单验证
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=5)
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'}) #captchaFiled字段会自动生成验证图片以及 一个input框


class ForgetPwdForm(forms.Form):
    email=forms.EmailField(required=True)
    # password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'}) # captchaFiled字段会自动生成验证图片以及 一个input框


class PwdRstForm(forms.Form):
    password = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


