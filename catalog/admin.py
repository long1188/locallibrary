from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)

# Register your models here.
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields=['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    #但如果你进一步将它们分组在元组中（如上述“日期”字段中所示），则会水平显示。


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# inlines:TabularInline stackedInline
class BookInstanceInline(admin.TabularInline):
    model = BookInstance


# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines=[BookInstanceInline]
'''
不幸的是，我们不能直接指定 list_display 中的 genre 字段，因为它是一个ManyToManyField （Django 可以防止这种情况，因为在这样做时会有大量的数据库访问“成本”）。相反，我们将定义一个
 display_genre 函数来获取信息作为一个字符串（这是我们上面调用的函数;下面我们将定义它）。'''
# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    #split the from into a without title,the other with availability title
    fieldsets=(
        (None,{'fields':('book','imprint','id')}),
        ('Availability',{'fields':('status','due_back')}),
    )


