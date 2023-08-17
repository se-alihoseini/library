from user.serializer import UserPassSerializer
from user.models import User, OtpCode


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class UserPassAuthentication(APIView):
    serializer_class = UserPassSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        srz_data = UserPassSerializer(data=request.data)
        if srz_data.is_valid():
            if User.check_user_pass(data=srz_data.validated_data):
                return Response(data='user pass is correct', status=status.HTTP_200_OK)
            return Response(data='user pass error', status=status.HTTP_400_BAD_REQUEST)
        return Response(data='validation error', status=status.HTTP_400_BAD_REQUEST)
