import  json
from django.shortcuts import render
from  django.http import  JsonResponse,HttpResponse
# Create your views here.
from  django.views.generic import TemplateView
from django.views.generic import View
from users.models import Banner,UserProfile,EmailVerifyRecord
from courses.models import Course
from organization.models import CourseOrg
from  .forms import UserAlterForm,ImageUploadForm,PassWdForm,RstEmailForm
import re
from django.contrib.auth.hashers import make_password,check_password
from  users.views import CustomBackend

from  utils.email_send import send_register_email

#--------------------------------网站首页-----------------------------------------------------
class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        # -----------------首页轮播块-----------------------
        index_banners = Banner.objects.all()

        # ---------------------首页课程块----------------------
        index_course_banner = Course.objects.all()[:2]
        index_course = Course.objects.all()[:6]
        index_class = []
        course_class_dict = {}
        for i in range(3, 9):
            index_class.append("module1_%s box" % i)
        for i in range(6):
            course_class_dict[index_class[i]] = index_course[i]
        # -----------------------首页机构块----------------------
        index_org = CourseOrg.objects.all()
        index_org_dict = {}
        for i in range(15):
            if ((i+1)%5)==0:
                index_org_dict[index_org[i]]="five"
                continue
            index_org_dict[index_org[i]]=""
        return render(request, 'index.html', {
            'index_banners': index_banners,
            'index_course_banner': index_course_banner,
            'course_class_dict': course_class_dict,
            'index_org_dict':index_org_dict,

        })

#----------------------------------用户中心首页--------------------------------------------

class UserCenterView(View):
    def get(self,request,user_id):
        return  render(request,'usercenter-info.html',{
        })

#-----------------用户在个人中心提交基本信息修改---------------------------------
class UserAlterView(View):
    def post(self,request):
        #实例化一个用户对象
        user=request.user
        #将后台传过来的数据保存
        new_nick_name = request.POST.get('nick_name', '')
        new_birth_day = request.POST.get('birth_day', '')
        new_address = request.POST.get('address', '')
        new_mobile = request.POST.get('mobile', '')
        # new_image=request.POST.get('image','')
        new_email=request.POST.get('email','')
        #实例化一个表单对象，表单数据为 从前台提交的POST请求数据
        user_alter_form = UserAlterForm(request.POST)
        #如果表单认证通过
        if user_alter_form.is_valid():
            user.nick_name=new_nick_name
            user.birday=re.sub(r'[\u4e00-\u9fa5]','',re.sub(r'[\u4e00-\u9fa5]','-',new_birth_day,2))
            user.address=new_address
            user.mobile=new_mobile
            # user.image=new_image
            user.save()
            result = {'status':'success','msg':'保存成功'}
            return JsonResponse(result)
        else:#用户表单修改提交不通过
            result={'status':'fail','msg':'修改失败'}
        #todo  增加错误提示功能，在前端将错误提示显示，并且显示具体错误信息

#--------------------------------修改头像提交-----------------------------------
class UserImageView(View):
    def post(self,request):
        #创建一个表单对象
        image_form=ImageUploadForm(request.POST,request.FILES)
        # image=request.POST.get('image','')
        if image_form.is_valid():
            image=image_form.cleaned_data['image']
            request.user.image=image
            request.user.save()
            return render(request,'usercenter-info.html')



#----------------------------------- 账号密码修改----------------------------------------
class UserPassWdView(View):
    def post(self,request):
        form=PassWdForm(request.POST)
        if form.is_valid():
            passwd1 = request.POST.get('password1', '')
            passwd2 = request.POST.get('password2', '')
            if passwd1 != passwd2:
                return JsonResponse({'status':'fail','msg':'密码不一致'})

            request.user.password=make_password(passwd1)
            request.user.save()
            return JsonResponse({'status':'success','msg':'修改成功,请重新登陆'})
        else:
            print(form.errors)
            result=json.dumps(form.errors)
            return JsonResponse(result)


#----------------------------发送邮箱验证码(get 获取)-------------------------------
class SendEmailCodeView(View):
    def get(self,request):
        email=request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return JsonResponse({'email':'邮箱已被绑定'})
        else:
            status=send_register_email(email,'update_email')
            if status:
                return  JsonResponse({'status':'success'})
            else:
                return  JsonResponse({'status':'failure'})


#----------------------------------输入验证码重新绑定邮箱(post提交)------------------------------------------
class RstEmailView(View):
    def post(self,request):
        email1=request.user.email
        form=RstEmailForm(request.POST)
        if form.is_valid():
            new_email=request.POST.get('email','')
            email_code=request.POST.get('code','')
            exist_codes_list=[]
            exist_email_objs=EmailVerifyRecord.objects.filter(email=new_email,send_type='update_email')
            for exist_email_obj in exist_email_objs:
                exist_codes_list.append(exist_email_obj.code)

            if email_code in exist_codes_list:
                if email_code==exist_codes_list[-1]:
                    user=request.user
                    user.email=new_email
                    # UserProfile.objects.filter(email=email1).update(email=new_email)
                    user.save()
                    return  JsonResponse({'status':'success','msg':'修改成功'})
                else:
                    return JsonResponse({'status':'failure','msg':'验证码已失效'})#只有最新的验证码起作用
            else:
                return JsonResponse({'status':'failure','msg':'验证码错误'})
        else:
            return JsonResponse({'email':'邮箱填写有误'})


#--------------------404--------------------------
def page_not_found(request):
    from  django.shortcuts import  render_to_response
    response=render_to_response('404.html',{})