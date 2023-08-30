from datetime import datetime, timedelta

from user import repositories
import redis
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from library import settings


def get_user(user_id):
    return repositories.get_user(user_id)


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


def send_sms(user_id, token, service_name):
    service_status = False
    while not service_status:
        if service_name == 'kave_negar':
            try:
                service_status = kave_negar(user_id, token)
            except:
                service_status = signal(user_id, token)
        else:
            try:
                service_status = signal(user_id, token)
            except:
                service_status = kave_negar(user_id, token)


def kave_negar(user_id, token):
    r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
    block_check = r.exists("kave_negar_block")
    half_open_check = r.exists("kave_negar_half_open")

    if block_check:
        return False
    elif half_open_check:
        try:
            print(f'kave_negar : {token} to {user_id}')
            r.delete('kave_negar_half_open')
            return True
        except:
            return False
    else:
        try:
            print(f'kave negar : {token} to {user_id}')
            return True
        except:
            r.setex('kave_negar_block', 60, '')
            r.set('kave_negar_half_open', '')
            return False


def signal(user_id, token):
    r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
    block_check = r.exists("signal_block")
    half_open_check = r.exists("signal_half_open")

    if block_check:
        return False
    elif half_open_check:
        try:
            print(f'signal : {token} to {user_id}')
            r.delete('signal_half_open')
        except:
            return False
    else:
        try:
            print(f'signal : {token} to {user_id}')
            return True
        except:
            r.setex('signal_block', 60, '')
            r.set('signal_half_open', '')
            return False
