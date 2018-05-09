from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from  django.contrib import auth
from  django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # Q支持传参内部的运算，and or not
from django.views.generic.base import View
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm,PwdRstForm
from django.contrib.auth.hashers import make_password,check_password
from utils.email_send import send_register_email
from  django.http import  HttpResponseRedirect


# ----------重写的后端验证方式-------
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            if user.check_password(password):
                return user
        except Exception as e:
            return None


# -----------用户登陆----------------------------
class LoginView(View):
    def get(self, request):
        login_form=LoginForm()
        return render(request, 'login.html',{'login_form':login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)  # 传入的POST表单的表单项名字必须与类中定义字段相同

        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)#验证是否匹配
            # 登陆
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    # return render(request, 'index.html',{'username':user_name})
                    return redirect(request.session.get('url', '/'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self,reqeust):
        auth.logout(request=reqeust)
        from  django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index:index'))



# -------用户注册-----------------
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            is_exist = UserProfile.objects.filter(email=user_name)
            if is_exist:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)  # query  sets
            user_profile.save()  # save query set

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


# --------用户激活--------------------
class ActiveUserView(View):
    def get(self, request, active_code):  #
        all_record = EmailVerifyRecord.objects.filter(code=active_code)  # 筛选出验证码问active_code的验证码表
        if all_record:  # 如果存在
            for record in all_record:  # 挨个遍历出来...
                email = record.email  # 取出外键关联
                user = UserProfile.objects.get(email=email)  # 获得email对应的userfile表格
                user.is_active = True  # 将邮箱状态设置为激活
                user.save()  # .
        else:
            return render(request, 'active_failed.html')
        return render(request, 'login.html')


# --------------------找回密码-------------------------
class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)  # form表单内只能传入dict

        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')#获取提交的邮箱
            # is_exist=UserProfile.objects.filter(email=email)
            send_register_email(email, 'forget')  # 发送邮件 模式为找回
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


# --------重新设置密码--------------------
class ResetView(View):
    def get(self, request, active_code):  #
        pwdrst_form = PwdRstForm(request.POST)
        all_record = EmailVerifyRecord.objects.filter(code=active_code)  # 筛选出验证码为active_code的验证码表
        if all_record:  # 如果存在
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email':email})
        else:
            return render(request, 'active_failed.html')

#--------修改密码----------------
class ModifyPwdView(View):
    def post(self,request):
        modify_form=PwdRstForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password','')
            pwd2=request.POST.get('password2','')
            email=request.POST.get('email','') #获取需要修改的账号的email
            if pwd1 == pwd2:
                user=UserProfile.objects.get(email=email)
                password=user.password
                if  check_password(pwd1,password):
                    return render(request,'password_reset.html',{'email':email,'msg':'新密码不能与旧密码重复'})
                pwd = make_password(pwd1)
                user.password=pwd
                user.save()
                return render(request,'login.html') #修改后返回主页
            else:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致'})
        else:
            email = request.POST.get('email', '')  # 获取需要修改的账号的email
            return render(request, 'password_reset.html', {'email': email, 'modify_form':modify_form})


