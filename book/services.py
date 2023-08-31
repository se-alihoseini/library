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


def book_reserves(days, user, book):
    if user.subscription_status:
        data = vip_user_reserves(days, user, book)
    else:
        data = normal_user_reserves(days, user, book)
    return data


def normal_user_reserves(days, user, book):
    if days > 7:
        raise ValueError('days cannot more than 7 days')
    else:
        cost = days*1000
        total_cost = discount_calculator(user=user, cost=cost)
        reserve = repositories.create_reservation(days, user, book, total_cost)
        return reserve


def vip_user_reserves(days, user, book):
    if days > 14:
        raise ValueError('days cannot more than 7 days')
    else:
        cost = 0
        reserve = repositories.create_reservation(days, user, book, cost)
        return reserve


def book_reserved_list(user):
    return repositories.get_book_reserved_list()


def discount_calculator(user, cost):
    reservation_count = repositories.get_3_month_user_books_count(user=user)
    if reservation_count > 3:
        cost = cost*0.7
        if repositories.get_2_month_user_books_cost(user=user) > 300000:
            cost = 0
    return cost
