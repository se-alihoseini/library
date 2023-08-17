from user.serializer import GeneratePasswordSerializer
from user.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class GeneratePassword(APIView):
    serializer_class = GeneratePasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        srz_data = GeneratePasswordSerializer(data=request.data)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            user = User.get_user(vd['email_phone'])
            user.generate_password()
            # send new password to user
            return Response(data='data', status=status.HTTP_200_OK)
        return Response(data='data', status=status.HTTP_400_BAD_REQUEST)
