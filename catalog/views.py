from django.shortcuts import render
from django.views import generic
from .models import Book,BookInstance,Author,Genre
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
# Create your views here.

class BookListView(generic.ListView):
    model=Book
    paginate_by = 2
    #在模板中，你可以使用名为object_list 或 book_list的模板变量（即通常为“the_model_name_list”），以访问书本列表。
    context_object_name = 'my_book_list'  # your own name for the list as a template variable
    #queryset=Book.objects.filter(title__icontains='war')[:5]
    template_name='books/my_arbitrary_template_name_list.html'

class AuthorListView(generic.ListView):
    model=Author
    #paginate_by = 1

class AuthorDetailView(generic.DetailView):
    model = Author
class BookDetailView(generic.DetailView):
    model = Book
    #分页方面,内置于基于类的通用列表视图


    #使用 GET 参数访问不同的页面 - 要访问第 2 页，你将使用 URL：/catalog/books/?page=2。

    ''' using function to explain the way it work
    def book_detail_view(request,pk):
    try:
        book_id=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")

    #book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'catalog/book_detail.html',
        context={'book':book_id,}
    )

    '''



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

'''
我们还可以覆盖get_context_data() ，以将其他上下文变量传递给模板
def get_context_data(self, **kwargs):
        #获取现有的上下文 Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # 添加新的上下文信息。Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context   #返回新的（更新的）上下文
'''