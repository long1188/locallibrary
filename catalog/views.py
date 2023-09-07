from django.shortcuts import render

from .models import Book,BookInstance,Author,Genre
# Create your views here.
def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_author=Author.objects.count()
    return render(request,'index.html',context={'num_books':num_books,'num_instance':num_instances,
                                                'num_instance_available':num_instances_available,
                                                'num_authors':num_author},)

"""在模版中，你首先调用 load 指定“ static”去添加此模版库（如下）。
静态加载后，你可以使用 static 模版标签，指定感兴趣的文件相对URL

链接 URL
<li><a href="{% url 'index' %}">Home</a></li>

"""