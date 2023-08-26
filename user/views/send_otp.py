from user.serializer import EmailPhoneSerializer
from user.models import User, OtpCode

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class SendOtp(APIView):
    serializer_class = EmailPhoneSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        srz_data = EmailPhoneSerializer(data=request.data)
        if srz_data.is_valid():
            email_phone = srz_data.validated_data['email_phone']
            user = User.get_user(email_phone)
            OtpCode.send_otp(user)
            return Response(data='otp was sent', status=status.HTTP_200_OK)
        return Response(data='validation error', status=status.HTTP_400_BAD_REQUEST)
