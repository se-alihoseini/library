from user.serializer import ChangePasswordSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ChangePassword(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        srz_data = ChangePasswordSerializer(data=request.data)
        if srz_data.is_valid():
            vd = srz_data.validated_data
            user = request.user
            user.set_password(vd['password'])
            user.save()
            return Response(data='data', status=status.HTTP_200_OK)
        return Response(data='data', status=status.HTTP_400_BAD_REQUEST)
