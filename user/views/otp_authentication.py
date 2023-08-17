from user.serializer import OtpAuthSerializer
from user.models import User

from django.contrib.auth import login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class OtpAuthentication(APIView):
    serializer_class = OtpAuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        srz_data = OtpAuthSerializer(data=request.data)
        if srz_data.is_valid():
            if User.check_user_pass(data=srz_data.validated_data):
                user = request.user
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                return Response(data={'refresh': str(refresh), 'access': str(access)}, status=status.HTTP_200_OK)
        return Response(data='validation error', status=status.HTTP_400_BAD_REQUEST)
