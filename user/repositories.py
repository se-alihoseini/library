from django.shortcuts import get_object_or_404
from wtforms import ValidationError

from user.models import User, Subscription, Transaction
from book.serializer import BookSerializer
from book.book_transfer import producer_node, consumer_node
from library import settings
from datetime import datetime, timedelta


def get_user(phone_or_email):
    if '@' in phone_or_email:
        try:
            user = User.objects.get(email=phone_or_email)
            return user
        except user.DoesNotExist:
            return None
    else:
        try:
            user = User.objects.get(phone_number=phone_or_email)
            return user
        except User.DoesNotExist:
            return None


def get_user_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        raise ValueError('user does not exist')



def set_subscription_for_user(user_id):
    user = get_user(user_id)
    subscription = Subscription.objects.get(user=user)
    now = datetime.now()
    if not subscription.is_active:
        subscription.start_date_at = now
        subscription.end_date_at = now + timedelta(days=31)
        subscription.is_active = True
    else:
        subscription.end_date_at += timedelta(days=31)
    try:
        subscription.save()
        return 'subscription saved'
    except:
        return 'subscription cant save'


def create_transaction(user_id, transaction_code):
    user = get_user(user_id=user_id)
    transaction = Transaction.objects.get(user=user, transaction_code=transaction_code)
    return transaction
