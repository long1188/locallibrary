from django.db import models

#Django 允许你定义一对一 (OneToOneField)，一对多 (ForeignKey) 和多对多 (ManyToManyField) 的关系。
from django.db import models
from django.urls import reverse
import uuid#unique book instances
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    name=models.CharField(max_length=200,help_text="Enter a book genre")
    def __str__(self):
        return self.name

class Book(models.Model):
    title=models.CharField(max_length=200)
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)#  # Author as a string rather than object because it hasn't been declared yet in the file.
    summary=models.TextField(max_length=1000,help_text="Enter a brief description of the book")
    isbn=models.CharField('ISBN',max_length=13,help_text='13 charater <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre=models.ManyToManyField(Genre,help_text='Select a genre for this book')
    def __str__(self):
        return self.title
    def  get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])
    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

    class Meta:
        ordering = ['title']


'''
author field are null=True, which allows the database to store a Null value if no author is selected, 
and on_delete=models.SET_NULL, which will set the value of the author to Null if the associated author record is deleted.'''

class BookInstance(models.Model):
    id =models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    book=models.ForeignKey('Book',on_delete=models.SET_NULL,null=True)
    imprint =models.CharField(max_length=200)
    due_back=models.DateField(null=True,blank=True)
    borrower=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    #让用户可以借用书本实例,个模型和用户之间关联
    LOAN_STATUS=(
        ('m','Maintenance'),
        ('o','On loan'),
        ('a','Available'),
        ('r','Reverved'),
    )
    status=models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='m',help_text='Book Availability')
    class Meta:
        ordering=["due_back"]
        #当前用户的权限，存在名为 {{ perms }}的模板变量中,
        #Django“app”中的特定变量名，来检查当前用户是否具有特定权限
        #{{ perms.catalog.can_mark_returned }}

        #使用 permission_required装饰器,PermissionRequiredMixin测试权限,param is the permission's name
        permissions=(("can_mark_returned","set book as returned"),)
    def __str__(self):
        return '%s(%s)' % (self.id,self.book.title)

    @property#添加一个属性，我们可以从模板中调用它
    def is_overdue(self):#空的due_back字段，会导致 Django 抛出错误
        if self.due_back and date.today()>self.due_back:
            return True
        return False

class Author(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True,blank=True)
    date_of_death=models.DateField('Died',null=True,blank=True)
    def get_absolute_url(self):
        return reverse('author-detail',args=[str(self.id)])

    def __str__(self):
        return '%s ,%s' % (self.last_name,self.first_name)
    class Meta:
        ordering = ['last_name']