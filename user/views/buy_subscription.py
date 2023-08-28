from user.serializer import OtpAuthSerializer
from user.models import User, OtpCode
from user import services

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BuySubscription(APIView):
    def get(self, request):
        user = request.user
        response = services.buy_subscription(user.id)
        if response:
            return Response(data='vip subscription was applied', status=status.HTTP_200_OK)
        else:
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

