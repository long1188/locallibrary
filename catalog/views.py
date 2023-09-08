from django.shortcuts import render
from django.views import generic
from .models import Book,BookInstance,Author,Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@permission_required('set book as returned')
def Liabrary_Listview(request):
    bookinstance_onloan = BookInstance.objects.filter(status__exact='o')
    return render(request, 'catalog/liabrary_list.html', context={'bookinstance_onloan': bookinstance_onloan}, )


# @permission_required('set book as returned')
# def Liabrary_Listview(request):
#     return render(request,'La')
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):#限制为当前用户的BookInstance对象,重新实现
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

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

''' @login_required this will redirect to the login URL defined in the project settings (settings.LOGIN_URL), 
passing the current absolute path as the next URL parameter. If the user succeeds in logging in 
then they will be returned back to this page, but this time authenticated.'''
@login_required#则会重定向到项目设置（settings.LOGIN_URL）中定义的登录 URL，并将当前绝对路径，
def index(request):#在基于类别class的视图中，限制对登录用户的访问的最简单方法，LoginRequiredMixin派生 class MyView(LoginRequiredMixin, View):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_author=Author.objects.count()
    num_visits=request.session.get('num_visits',0)#我们首先得到'num_visits'会话密钥的值，如果之前没有设置，则将值设置为 0。
    request.session['num_visits']=num_visits+1
    return render(request,'index.html',context={'num_books':num_books,'num_instance':num_instances,
                                                'num_instance_available':num_instances_available,
                                                'num_authors':num_author,'num_visits':num_visits},)

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
