from book.serializer import BookSerializer
from book.models import Book
from book import services

from django.shortcuts import get_object_or_404
import json

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


class BookCrud(ViewSet):
    serializer_class = BookSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        srz_data = BookSerializer(data=request.data)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            title = vd['title']
            description = vd['description']
            publication_date = vd['publication_date']
            isbn = vd['isbn']
            price = vd['price']
            author = vd['author']
            genre = vd['genre']
            book = services.create_book(title, description, publication_date, isbn, price, author, genre)
            if book:
                return Response(data='book was created', status=status.HTTP_200_OK)
        return Response(data=srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        book = services.get_book_by_id(pk)
        srz_data = BookSerializer(instance=book)
        return Response(data=srz_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        srz_data = BookSerializer(instance=book, data=request.data, partial=True)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            title = vd['title']
            description = vd['description']
            publication_date = vd['publication_date']
            isbn = vd['isbn']
            price = vd['price']
            author = vd['author']
            genre = vd['genre']
            updated_book = services.update_book(pk, title, description, publication_date, isbn, price, author, genre)
            if updated_book:
                return Response('book was updated', status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        services.delete_book(pk)
        return Response(data='book was deleted', status=status.HTTP_200_OK)

    def list(self, request):

        page = self.request.query_params.get('page')
        genre_query = self.request.query_params.getlist('genre', '')
        int_genre = [int(value) for value in genre_query]
        city_query = self.request.query_params.get('city', '')
        int_city = [int(value) for value in city_query]
        min_price_query = request.GET.get('min_price', 0)
        max_price_query = request.GET.get('max_price', float('inf'))
        query_filter = self.request.query_params.get('q', '')
        query_sort = self.request.query_params.get('sort', '')

        books = services.list_of_books(page, query_filter, query_sort, min_price_query, max_price_query, int_genre,
                                       int_city)
        data_list = [json.loads(json.dumps(book, default=str)) for book in books]

        data = {'mongo': data_list}
        return Response(data=data, status=status.HTTP_200_OK)
