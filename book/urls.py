from book.views import book_crud
from django.urls import path

from rest_framework import routers

appname = 'book'

urlpatterns = [
]

router = routers.SimpleRouter()
router.register('book', book_crud.BookCrud, basename='book')
urlpatterns += router.urls
