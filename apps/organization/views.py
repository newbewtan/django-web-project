from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render_to_response,HttpResponse
from django.http import  HttpResponse,JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from .models import CourseOrg,CityDict
from courses.models import Course
from organization.models import Teachers
from  django.contrib import auth
from operation.models import UserFavorite,UserProfile
from  django.db.models import Q

# Create your views here.


#--------------------------------机构列表页面--------------------------
class OrgListView(View):
    '''课程机构列表'''
    def get(self,request):
        all_orgs=CourseOrg.objects.all()#获取所有课程机构
        hot_orgs=all_orgs.order_by("-click_nums")[:3]
        all_citys=CityDict.objects.all()#获取所有的城市信息
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # todo 对结果集再次筛选，name__icontains 表示对名字进行通配匹配，i表示不区分大小写.
            # 课程搜索
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(category__icontains=search_keywords))

        #取出筛选城市
        city_id=request.GET.get('city','')#检测用户在前端的筛选选择
        if city_id:#一旦检测到，对机构进行对应筛选
            all_orgs=all_orgs.filter(city_id=city_id)
        #类别筛选
        category=request.GET.get('ct','')
        if category:#选择种类
            all_orgs=all_orgs.filter(category=category)

        sort=request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_orgs=all_orgs.order_by('-students')
            elif sort=='courses':
                all_orgs = all_orgs.order_by('-course_nums')
        org_nums = all_orgs.count()  # 筛选后机构数量
        #对课程机构进行分页
        try:
            #取页面
            page = request.GET.get('page', 1) #确保获取的值为一个整数的值，如果不是，就返回首页
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,5,request=request)#对所有的数据进行分页处理
        orgs = p.page(page)#page_obj ,页面对象，每页内包含的机构

        return  render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort

        })




#-------------------------------------用户咨询表单提交----------------------------------------
class AddAskView(View):
    '''用户添加咨询'''
    def post(self,request):
        userask_form=UserAskForm(request.POST)#modelform的保存方式
        if userask_form.is_valid():#如果满足条件，将成功提交数据到数据库
            userask_form.save(commit=True)#提交数据
            result={'status':'success'}#返回结果
            return  JsonResponse(result)

        else:#不满足不提交保存
            result={'status':'fail','msg':'提交失败！'}
            return JsonResponse(result)


#--------------------------------------------机构详情主页面---------------------------------------
class OrgDetailHomeView(View):
    '''
    机构详情页首页
    '''
    def get(self,request,org_id):#传入课程机构的id
        current_page = 'home'
        course_org=CourseOrg.objects.get(id=int(org_id)) #通过机构id获取到对应的课程机构--信息
        all_courses=course_org.course_set.all()[:3] #获取到所有课程的所有信息
#   可通过外键的方式反向索引获取 获取到设置外键的表单的内容
#   用法为 外键实例.设置外键的表单名(小写)+ '_' +'set'

    #------判断是否收藏--------
        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=org_id,fav_type=2):
                has_fav=True

        all_teachers=course_org.teachers_set.all()[:2]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'org_id':org_id,
            'current_page':current_page,
            'has_fav':has_fav
        })


#------------------------------------------------机构课程页面---------------------------------------------
class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))#课程机构
        all_courses = course_org.course_set.all()#获取机构的所有课程
        print(all_courses)
        # 总机构数目
        course_nums = all_courses.count()

        # ------判断是否收藏--------
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True

        # 对课程机构进行分页
        try:
            # 取页面
            page = request.GET.get('page', 1)  # 确保获取的值为一个整数的值，如果不是，就返回首页
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 8, request=request)  # 对所有的数据进行分页处理
        courses = p.page(page)  # page_obj ,页面对象，每页内包含的课程数
        return  render(request,'org-detail-course.html',{
            'org_id':org_id,
            'course_org': course_org,
            'all_courses':all_courses,
            'course_nums':course_nums,
            'courses':courses,
            'current_page': current_page,
            'has_fav': has_fav
        })



#-----------------------------------------------机构介绍页面---------------------------------------------
class OrgDescView(View):
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # ------判断是否收藏--------
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True

        return  render(request,'org-detail-desc.html',{
            'org_id':org_id,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })



#--------------------------------------------机构老师页面------------------------------------------
class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page='teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # ------判断是否收藏--------
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        all_teachers=course_org.teachers_set.all()

        return  render(request,'org-detail-teachers.html',{
            'org_id':org_id,
            'course_org': course_org,
            'all_teachers':all_teachers,
            'current_page': current_page,
            'has_fav': has_fav
        })



#---------------------------------------------用户收藏/取消收藏----------------------------------------
class AddFavView(View):
    '''
    用户收藏/取消收藏
    '''
    def post(self,request):

        fav_id=request.POST.get('fav_id','0') #
        fav_type=request.POST.get('fav_type','0')#
        if not request.user.is_authenticated():
            #判断用户是否登陆
            result = {'status': 'fail', 'msg': '用户他妈的未登陆！'}
            return JsonResponse(result)
        #定义已存在的记录
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        userprofile = UserProfile.objects.get(username=request.user)
        if exist_records:
            #已经存在表示用户取消收藏
            exist_records.delete()
            result = {'status': 'fail', 'msg': '收藏！'}
            return JsonResponse(result)
        else:
            user_fav=UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.fav_id=fav_id
                user_fav.fav_type=fav_type
                user_fav.user_id=userprofile.id
                user_fav.save()
                result = {'status': 'success', 'msg': '收藏成功！'}
                return JsonResponse(result)
            else:
                result = {'status': 'fail', 'msg': '收藏失败！'}
                return JsonResponse(result)