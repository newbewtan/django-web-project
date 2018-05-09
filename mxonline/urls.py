"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import xadmin
# from  django.views.generic import TemplateView
from  django.views.generic import TemplateView
from django.views.static import serve
from mxonline.settings import MEDIA_ROOT,STATIC_URL

from  users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView,ModifyPwdView



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #--------------------用户中心首页-------------------------
    url('^', include('operation.urls',namespace='index')),
    # 配置上传文件的访问处理函数 用于读取后台的/media/...下的文件
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    #配置浏览器获取静态文件路径，用于读取/static/下的文件
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_URL}),
    #-----------命名空间----------------------
    #用户中心URL配置
    url(r'^user/',include('users.urls',namespace='user')),
    #课程机构URL配置
    url(r'^org/', include('organization.urls',namespace='org')),
    #课程相关URL配置
    url(r'^course/', include('courses.urls', namespace='courses')),
    #授课教师相关URL配置
    url(r'^teachers/',include('teachers.urls',namespace='teachers')),
    #验证码
    url(r'^captcha/', include('captcha.urls')),

]


# 以下代码可用于开发者在开发阶段使用静态文件

# from . import settings
# if settings.DEBUG:
#    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#                                    {'document_root': settings.MEDIA_ROOT }),
#         url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}), )
#
#全局404函数定义
handler404='operation.views.page_not_fand'