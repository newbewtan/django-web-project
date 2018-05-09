from django.shortcuts import render
from django.views.generic.base import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from users.models import UserProfile
from  operation.models import  UserFavorite,UserCourse,CourseComments
from organization.models import CourseOrg
from courses.models import Video,Lesson,CourseResource
from  random import  randint
from  django.http import JsonResponse,HttpResponse
from  django.db.models import  Q


#-------------------------课程列表页---------------------------
class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.all() #获取所有的课程
        hot_courses=all_courses[:3]
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            #todo 对结果集再次筛选，name__icontains 表示对名字进行通配匹配，i表示不区分大小写.
            #课程搜索
            all_courses=all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))


        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-fav_nums')
        course_nums=all_courses.count()
        try:
            page = request.GET.get('page', 1)
        except:
            page=1
        p = Paginator(all_courses, 9, request=request)
        courses=p.page(page)# 我是从这个视图里面传一个主键 course.id到 CourseDetailView 里面去

        return  render(request,'course-list.html',{
            'all_courses':all_courses,
            'hot_courses':hot_courses,
            'courses':courses,
            'sort':sort,
        })


#------------------课程详情页-----------------
class CourseDetailView(View): #这是我的视图 公开课
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        # user=course.userprofile_set.all()[:1]
        users=UserProfile.objects.filter(course=course)
        if users:
            user=users[0]
        else:
            user=None

        #获取课程
        org=course.course_org#org_id=1
        #------处理用户机构收藏-------------

        org_has_fav=False
        if request.user.is_authenticated():#首先判断登陆了没有
            user=request.user
            fav=UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2)
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                org_has_fav = True
        #其他课程推荐，如果存在下一个课程，那就推出下一个，如果不存在下一个课程吗，就推出上一个课程

        all_course=Course.objects.all()
        other_id=randint(1,len(all_course))
        while other_id == int(course_id):
            other_id=randint(1,len(all_course))
        other_course=Course.objects.get(id=other_id)

        return render(request,'course-detail.html',{
            'course':course,
            'user':user,
            'other_course':other_course,
            'org_has_fav':org_has_fav
        })


#------------------------------------------课程视频-----------------------------------------------
class CourseVideoView(View):
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        a=str(course)
        teacher =course.teacher
        #------------------学过该课的还学过-----------
        users=course.userprofile_set.all()[:2]#获取到学习了本课程的前两位学生
        course_list=[]#创建一个空的列表保存
        all_course_res=CourseResource.objects.filter(course=course)
        for user in users:
            user_id=user.id#获取到学生的id
            user_course_objs=UserCourse.objects.filter(user_id=user_id)
            for user_course_obj in user_course_objs:
                user_course=Course.objects.get(id=user_course_obj.course_id)
                b=str(user_course)
                if str(user_course) != str(course):
                    course_list.append(user_course)
        course_list=course_list[:3]#取两名学生总课程的前三个
        # --------加入文章文件视频目录---------------------
        all_lessons=Lesson.objects.filter(course=course).order_by('add_time')

        return  render(request,'course-video.html',{
            'course':course,
            'teacher':teacher,
            'course_list':course_list,
            'all_lessons':all_lessons,
            'all_course_res':all_course_res
        })

#-------------------------------------课程评论-------------------------------------------

class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.filter(id=int(course_id))[0]
        # a = str(course)
        teacher = course.teacher
        # ------------------学过该课的还学过-----------
        users = course.userprofile_set.all()[:2]  # 获取到学习了本课程的前两位学生
        course_list = []  # 创建一个空的列表保存
        for user in users:
            user_id = user.id  # 获取到学生的id
            user_course_objs = UserCourse.objects.filter(user_id=user_id)
            for user_course_obj in user_course_objs:
                user_course = Course.objects.get(id=user_course_obj.course_id)
                b = str(user_course)
                if str(user_course) != str(course):
                    course_list.append(user_course)
        course_list = course_list[:3]  # 取两名学生总课程的前三个
        # --------加入文章文件视频目录---------------------
        all_lessons = Lesson.objects.filter(course=course).order_by('add_time')

        #---------------显示用户评论----------------------
        use_comm_dict={}
        all_comments=CourseComments.objects.all().order_by('-add_time')

        all_users=UserProfile.objects.all()


        return render(request, 'course-comment.html', {
            'course': course,
            'teacher': teacher,
            'course_list': course_list,
            'all_lessons': all_lessons,
            'all_comments':all_comments,
            'all_users':all_users
        })

# ------------------------------------用户添加评论----------------------------------------------

class AddCommentView(View):
    # 用户提交评论
    def post(self,request):
        comment=request.POST.get('comments','')
        course_id=request.POST.get('course_id','0')
        if not request.user.is_authenticated():
            result = {'status': 'fail','msg': '用户他妈的未登录'}
            return JsonResponse(result)
        if comment=='':
            result={'status': 'success','msg':'评论不能为空'}
            return JsonResponse(result)
        course_comment=CourseComments()#创建一个心得评论论实例
        course_comment.user_id=request.user.id
        course_comment.course_id=course_id
        course_comment.comments=comment
        course_comment.save()

        result={'status': 'success','msg': '评论成功'}
        return JsonResponse(result)

#---------------------------课程视频播放----------------------------------
class CoursePlayView(View):
    def get(self, request, video_id):
        video=Video.objects.get(id=int(video_id))
        course = video.lesson.course
        teacher = course.teacher
        # ------------------学过该课的还学过-----------
        users = course.userprofile_set.all()[:2]  # 获取到学习了本课程的前两位学生
        course_list = []  # 创建一个空的列表保存
        all_course_res = CourseResource.objects.filter(course=course)
        for user in users:
            user_id = user.id  # 获取到学生的id
            user_course_objs = UserCourse.objects.filter(user_id=user_id)
            for user_course_obj in user_course_objs:
                user_course = Course.objects.get(id=user_course_obj.course_id)
                if str(user_course) != str(course):
                    course_list.append(user_course)
        course_list = course_list[:3]  # 取两名学生总课程的前三个
        # --------加入文章文件视频目录---------------------
        all_lessons = Lesson.objects.filter(course=course).order_by('add_time')

        return render(request, 'course-play.html', {
            'video':video,
            'course': course,
            'teacher': teacher,
            'course_list': course_list,
            'all_lessons': all_lessons,
            'all_course_res': all_course_res
        })