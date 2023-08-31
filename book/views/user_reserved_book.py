from book.serializer import BookListSerializer
from book.services import book_reserved_list

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserReservedBook(APIView):
    def get(self, request):
        books = book_reserved_list(user=request.user)
        srz_data = BookListSerializer(instance=books)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)
