from django.urls import path,re_path
from catalog import views
import re

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('books/<int:pk>',views.BookDetailView.as_view(),name='book-detail'),
    path('authors/',views.AuthorListView.as_view(),name="authors"),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

]
#加上一个定义数据类型的转换器规范:int，str，slug，uuid，path
#'<int:pk>' 来捕获 book id，它必须是一个整数，并将其作为名为 pk 的参数（主键的缩写）传递给视图
#re_path正则表达式
#re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
#(?P<name>...)
#它还捕获所有数字（?P<pk>\d+），并将它们传递给名为 'pk' 的参数中的视图。捕获的值始终作为字符串传递！

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('liabrary/', views.Liabrary_Listview, name='all-borrowed'),
]

'''
[]匹配集合中的一个字符。例如，[abc] 将匹配 'a' 或 'b' 或 'c'。
 [-\w] 将匹配 ' - ' 字符，或任何单词字符。
 \w 匹配单词字符，例如字母，数字或下划线字符（_）中的任何大写或小写字符
'''

'''
要对多个资源，使用相同的视图，
URL 中传递其他选项,被声明为一个字典{'my_template_name': 'some_path'}, 
'''
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
#path('book/<uuid:pk>/renew1/', views.RenewBookModelForm, name='renew-modelform-librarian'),
#re_path('book/(?P<id>\d+)/$', views.RenewBookModelForm),
]
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]
