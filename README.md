### django-web-project
> 用xadmin打造后台的一个前后端不分离django web项目

#### django项目开发笔记

##### 1.通过request.path的位筛选进行active锁定，比如说项目中的首页、课程页等主页的高亮锁定
```
<li  {% if request.path|slice:'7' == '/course' %}class="active"{% endif %}><a href="{% url 'index:index' %}">首页</a></li>   
```
 **request.path**返回的是不包含域名的url，"|"表示进行过滤，是django template的一个filter，slice是筛选位数。
 
 
 
##### 2.django中进行keyword模糊输入进行数据库筛选

![Alt text](E:/谭志勇/有道云笔记_markdown/image/通配筛选.png)
需要做到：左侧choice为选择栏目，筛选结果类型，输入框输入通配字符，点击按钮响应将通配数据从数据库中抓取出显示到前端页面
```
class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.all() #获取所有的课程
        hot_courses=all_courses[:3]
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            #todo 对结果集再次筛选，name__icontains 表示对名字进行通配匹配，i表示不区分大小写.
            #课程搜索
            all_courses=all_courses.filter(name__icontains=search_keywords)
```
实现方法：通过在url中添加keyword实现，


###### 3. django的Q对象支持传参内部的运算，and or not
```
from django.db.models import Q

   user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 
  
```
文中Q(a1)|Q(a2)相当于a1或者a2，属于一种或操作,转换成sql就相当于
>select * from UserProfile where username=username or email=username
```
  user = UserProfile.objects.get(Q(username=username) $ Q(email=username))  # 
```
同理，Q对象的"&"相当于与操作，既"and"
```
  user = UserProfile.objects.get(~Q(username=username)  )  # 
```
"~"相当于非也就是sql中的 "not"
```
  user = UserProfile.objects.get(Q(username=username)， Q(email=username))  # 
```
值得注意的是，多个Q对象共存相当于 "and"且的关系


form将用户传递过来的数据进行预处理


#### django前台template支持过滤器作用，| 
