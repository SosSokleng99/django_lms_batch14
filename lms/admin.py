from django.contrib import admin

# Register your models here.
from .models import Genre, Book, BookInstance

# admin.site.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'display_genre']



admin.site.register(Book, BookAdmin)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['__str__' ,'status', 'imprint', 'due_back']

    list_filter = ('status', 'due_back')

admin.site.register(BookInstance, BookInstanceAdmin)


admin.site.register(Genre)
