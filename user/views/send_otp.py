from user.serializer import EmailPhoneSerializer
from user.models import User, OtpCode
from user.services import send_sms, get_user

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
import asyncio

import redis
from library import settings


class SendOtp(APIView):
    serializer_class = EmailPhoneSerializer
    permission_classes = (AllowAny,)

    # @method_decorator(ratelimit(key='user', rate='5/2m', method='POST', block=True))
    # @method_decorator(ratelimit(key='user', rate='10/h', method='POST', block=True))
    def post(self, request):
        srz_data = EmailPhoneSerializer(data=request.data)
        if srz_data.is_valid():
            email_phone = srz_data.validated_data['email_phone']
            user = get_user(email_phone)
            code = OtpCode.create_otp(user)
            asyncio.run(send_sms(user_id=user.id, token=code.code))

            r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
            # r.delete('signal_block')
            all_keys = r.keys('*')
            all_values = r.mget(all_keys)
            return Response(data={'keys': all_keys, 'values': all_values}, status=status.HTTP_200_OK)
        return Response(data='validation error', status=status.HTTP_400_BAD_REQUEST)
