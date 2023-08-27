from book import repositories


def create_book(title, description, publication_date, isbn, price, author, genre):
    return repositories.create_book(title, description, publication_date, isbn, price, author, genre)


def get_book_by_id(book_id):
    return repositories.get_book_by_id(book_id)


def update_book(book_id, title, description, publication_date, isbn, price, author, genre):
    return repositories.update_book(book_id, title, description, publication_date, isbn, price, author, genre)


def list_of_books(page, query_filter, query_sort, min_price_query, max_price_query, int_genre, int_city):
    return repositories.get_all_books(page, query_filter, query_sort, min_price_query, max_price_query, int_genre
                                             , int_city)


def delete_book(pk):
    return repositories.delete_book(pk)


def book_reserves(self):
    pass


def book_reserved_list(self):
    pass


def reserves_cost_calculator(self):
    pass


def discount_calculator(self):
    pass

