import random

from user import repositories
import redis
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from library import settings
import requests


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


async def send_sms(user_id, token):
    service_status = False
    while not service_status:
        r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
        keys = r.keys('sms_service:*')
        values = r.mget(keys)
        values_list = list(values)

        key_count = len(keys)
        number = random.randint(1, key_count)-1
        method = eval(values_list[number].decode('utf-8'))
        service_status = method(user_id, token)


def create_sms_service_in_redis(service_name, service_method):
    r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
    r.set(f'sms_service:{service_name}', f'{service_method}')
    r.set(f'sms_service_error:{service_name}', '0')


def kave_negar_service(user_id, token):
    r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
    block_check = r.exists("kave_negar_block")

    if block_check == 1:
        value = r.get('kave_negar_block')
        return False
    else:
        # sms_service_response = requests.post(url='', data='')
        sms_service_response = 200
        if sms_service_response == 200:
            print(f'kave negar : {token} to {user_id}')
            return True
        else:
            num = r.incr('sms_service_error:kave_negar')
            if num >= 3:
                r.setex('kave_negar_block', '1800', '')
                r.set('sms_service_error:kave_negar', '0')
                return False


def signal_service(user_id, token):
    r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
    block_check = r.exists("signal_block")

    if block_check == 1:
        return False
    else:
        # sms_service_response = requests.post(url='', data='')
        sms_service_response = 20
        if sms_service_response == 200:
            print(f'signal : {token} to {user_id}')
            return True
        else:
            num = r.incr('sms_service_error:signal')
            if num >= 3:
                r.setex('signal_block', '1800', '')
                r.set('sms_service_error:signal', '0')
                return False
