from django.contrib import admin
from book.models import Book, Author, City, Genre

admin.site.register(Author)
admin.site.register(City)
admin.site.register(Genre)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'isbn', 'is_deleted')
    fields = ('title', 'author', 'genre', 'publication_date', 'isbn', 'price', 'is_deleted')
