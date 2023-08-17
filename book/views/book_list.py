from book.serializer import BookListSerializer
from book.models import Book

from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class BookList(APIView):
    def get(self):
        books = Book.objects.filter(is_deleted=False)
        srz_data = BookListSerializer(instance=books, many=True)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
