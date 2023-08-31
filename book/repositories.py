from book.models import Book
from book.serializer import BookSerializer
from book.models import Reservation
from book.book_transfer import producer_node, consumer_node
from library import settings

from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
import datetime


def get_all_books(page, query_filter, query_sort, min_price_query, max_price_query, int_genre, int_city):
    if query_sort == 'ascending':
        sort = 1
    else:
        sort = -1
    mongo_db = settings.MONGO_DB['mongo_db']
    collection = mongo_db['book']
    pipeline = [
        {"$match":
             {"$or": [{"title": {"$regex": query_filter}},
                      {"description": {"$regex": query_filter}}],
              "is_deleted": False,
              "genre": {"$in": int_genre} if int_genre else {"$exists": True},
              "author_city": {"$in": int_city} if int_city else {"$exists": True},
              "price": {"$gte": int(min_price_query), "$lte": float(max_price_query)},
              }},
        {"$sort": {"price": sort}},
        {"$skip": (int(page) - 1) * 10} if page else {"$skip": 0},
        {"$limit": 10}
    ]
    print(pipeline)
    books = list(collection.aggregate(pipeline))
    return books


def get_book_by_id(book_id):
    return get_object_or_404(Book, pk=book_id, is_deleted=False)


def update_book(book_id, title, description, publication_date, isbn, price, author, genre):
    book = get_book_by_id(book_id)
    book.title = title
    book.description = description
    book.publication_date = publication_date
    book.isbn = isbn
    book.price = price
    book.author = author
    book.genre.add(*genre)
    book.save()
    data = BookSerializer(instance=book)
    producer_node.pr_create_object_mongo(message=str(data.data))
    consumer_node.co_create_object_mongo(callback='callback_mongo_update')
    return book


def delete_book(book_id):
    book = get_object_or_404(Book, pk=book_id, is_deleted=False)
    book.is_deleted = True
    book.save()
    data = BookSerializer(instance=book)
    producer_node.pr_create_object_mongo(message=str(data.data))
    consumer_node.co_create_object_mongo(callback='callback_mongo_update')


def create_book(title, description, publication_date, isbn, price, author, genre):
    book = Book.objects.create(title=title, description=description, publication_date=publication_date, isbn=isbn,
                               price=price, author=author)
    book.genre.add(*genre)
    book.save()
    author_city = book.author.city.id
    data = BookSerializer(instance=book)
    validate_data = data.data
    validate_data['author_city'] = author_city
    try:
        producer_node.pr_create_object_mongo(message=str(validate_data))
        consumer_node.co_create_object_mongo(callback='callback_mongo_create')
    except:
        book.delete()
    return book


def create_reservation(book, user, days, cost):
    now = datetime.date.today()
    first_book_version = book.version
    end_data = now + datetime.timedelta(days)
    reservation = Reservation.objects.create(book=book, user=user, end_date=end_data, cost=cost)
    new_book_version = book.version + 1
    if book.version == new_book_version:
        reservation.delete()
        raise ValidationError('reserve days cannot more than 14 days')
    else:
        book.version = new_book_version
        book.save()
    return reservation


def get_3_month_user_books_count(user):
    current_date = datetime.now()
    three_months_ago = current_date - datetime.timedelta(days=90)
    return Reservation.objects.filter(user=user, start_date__gte=three_months_ago).count()


def get_2_month_user_books_cost(user):
    current_date = datetime.now()
    three_months_ago = current_date - datetime.timedelta(days=60)
    return Reservation.objects.filter(user=user, start_date__gte=three_months_ago).aggregate(total=Sum('cost'))


def get_book_reserved_list(user):
    return Book.objects.filter(books_reserved__user_id=user.id)