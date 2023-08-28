from user import services

from rest_framework.views import APIView
from rest_framework.response import Response


class OrderVerifyView(APIView):
    def get(self, request, authority):
        user = request.user
        response = services.payment_verify( user_id=user.id)
        return Response(data=response['data'], status=response['status'])
