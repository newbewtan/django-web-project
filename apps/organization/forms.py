# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/3/27 16:17'
from  django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):#表单form的modelform形式
    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']
