from book.serializer import BookReserveSerializer
from book.services import book_reserves

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BookReserve(APIView):
    serializer_class = BookReserveSerializer

    def post(self, request):
        srz_data = BookReserveSerializer(data=request.data)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            book = vd['book']
            days = vd['days']
            response = book_reserves(book=book, user=request.user, days=days)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
