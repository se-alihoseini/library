from book.serializer import BookSerializer, BookListSerializer
from book.models import Book

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class BookCrud(ViewSet):
    serializer_class = BookSerializer

    def create(self, request):
        srz_data = BookSerializer(data=request.data)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            srz_data.create(validated_data=vd)
            return Response(data='book was created', status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        book = get_object_or_404(Book, pk=pk, is_deleted=False)
        srz_data = BookSerializer(instance=book)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request):
        pass

    def destroy(self, request, pk):
        book = get_object_or_404(Book, pk=pk, is_deleted=False)
        book.is_deleted = True
        return Response(data='book was deleted', status=status.HTTP_200_OK)
