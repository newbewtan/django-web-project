# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/4/13 10:27'

from  django import forms
from users.models import UserProfile,EmailVerifyRecord


class UserAlterForm(forms.ModelForm):#表单form的modelform形式
    class Meta:
        model=UserProfile
        fields=['nick_name','address','mobile','email','image']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['image']

class  PassWdForm(forms.Form):
    #最少5个字符，最多20个字符
    password1 = forms.CharField(required=True, min_length=5,max_length=20)
    password2 = forms.CharField(required=True, min_length=5, max_length=20)

class RstEmailForm(forms.ModelForm):
    class Meta:
        model=EmailVerifyRecord
        fields=['email','code']
