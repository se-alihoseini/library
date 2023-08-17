from book.views import book_crud, book_list
from django.urls import path

from rest_framework import routers

appname = 'book'

urlpatterns = [
    path('book/list/', book_list.BookList.as_view(), name='book_list')
]

router = routers.SimpleRouter()
router.register('book', book_crud.BookCrud, basename='book')
urlpatterns += router.urls
