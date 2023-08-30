from user.serializer import OtpAuthSerializer
from user.models import User, OtpCode
from user.services import user_login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class OtpAuthentication(APIView):
    serializer_class = OtpAuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        srz_data = OtpAuthSerializer(data=request.data)
        if srz_data.is_valid():
            email_phone = srz_data.validated_data['email_phone']
            code = srz_data.validated_data['code']
            user = User.get_user(email_phone)
            if OtpCode.check_otp(code=code, user=user):
                token = user_login(request, user)
                return Response(data=token, status=status.HTTP_200_OK)
        return Response(data='validation error', status=status.HTTP_400_BAD_REQUEST)
