from datetime import datetime, timedelta

from user import repositories
import redis
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from library import settings


def payment_service(amount, user_id):
    user = repositories.get_user(user_id)
    # data = {
    #     "MerchantID": settings.MERCHANT,
    #     "Amount": amount,
    #     "Description": 'description',
    #     "Phone": user.phone_number,
    #     "CallbackURL": 'http://192.168.1.21:8000/payment/verify',
    # }
    # data = json.dumps(data)
    # headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    # try:
    #     response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
    #     if response.status_code == 200:
    #         response = response.json()
    #         if response['Status'] == 100:
    #        return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
    #        'authority': response['Authority']}
    #         else:
    #             return {'status': False, 'code': str(response['Status'])}
    #     return response
    #
    # except requests.exceptions.Timeout:
    #     return {'status': False, 'code': 'timeout'}
    # except requests.exceptions.ConnectionError:
    #     return {'status': False, 'code': 'connection error'}
    data = {'data': True, 'status': 200}
    return data


def payment_verify(user_id):
    user = repositories.get_user(user_id)
    # data = {
    #     "MerchantID": settings.MERCHANT,
    #     "Amount": 200000,
    #     "Authority": authority,
    # }
    # data = json.dumps(data)
    # headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    # response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    #
    # if response.status_code == 200:
    #     response = response.json()
    #     if response['Status'] == 100:
    #          return {'status': True, 'RefID': response['RefID']}
    #     else:
    #         return {'status': False, 'code': str(response['Status'])}
    # return response
    data = {'data': True, 'status': 200, 'transaction_code': 'transaction_code'}
    if data['data']:
        try:
            repositories.create_transaction(user_id=user_id, transaction_code=data['transaction_code'])
            return buy_subscription(user_id, transaction_code=data['transaction_code'])
        except:
            raise 'error'
    return data


def buy_subscription(user_id, transaction_code):
    py_response = payment_service(amount=200000)
    if py_response:
        repositories.set_subscription_for_user(user_id=user_id, transaction_code=transaction_code)
        return True


def user_login(request, user):
    login(request, user)
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    return {'refresh': str(refresh), 'access': str(access)}


def send_sms(user_id, token, service_name):
    pass


def create_otp():
    pass


def delete_expired_otp():
    pass


def store_blocked_token(token, user_id):
    r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
    r.set(f"{token}", f"{user_id}")
    decoded_data = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    exp_date = decoded_data['exp']
    r.expireat(f"{token}", exp_date)
