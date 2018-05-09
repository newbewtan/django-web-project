from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.views.generic.base import View
from organization.models import  Teachers
from  django.db.models import  Q



class TeacherListView(View):
    def get(self,request):
        all_teachers=Teachers.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # todo 对结果集再次筛选，name__icontains 表示对名字进行通配匹配，i表示不区分大小写.
            # 课程搜索
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords))

        #按人气排行(点击人数，实际上是可以做点击收藏转换比来获取热度)
        sort=request.GET.get('sort','')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')
            # 对课程机构进行分页
        goal_teacher=Teachers.objects.filter(work_position='金牌讲师')
        goal_teacher=goal_teacher.order_by('-work_years')[:3]
        all_nums=all_teachers.count()

        try:
                # 取页面
            page = request.GET.get('page', 1)  # 确保获取的值为一个整数的值，如果不是，就返回首页
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 5, request=request)  # 对所有的数据进行分页处理
        teachers = p.page(page)  # page_obj ,页面对象，每页内包含的课程数
        return  render(request,'teachers-list.html',{
            'all_teachers':all_teachers,
            'goal_teacher':goal_teacher,
            'sort':sort,
            'all_nums':all_nums,
            'teachers':teachers
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        return  render(request,'teacher-detail.html',{

        })
