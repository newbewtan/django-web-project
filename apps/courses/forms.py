# -*- coding:utf-8 -*-
__author__ = 'bobby'
__date__ = '2018/4/9 15:17'
from  django import forms
from  .views import AddCommentView
from operation.models import CourseComments

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields=['comments']#对表中的具体字段进行验证
