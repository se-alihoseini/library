from user import services

from rest_framework.views import APIView
from rest_framework.response import Response


class PayView(APIView):
    def get(self, request):
        user = request.user
        response = services.payment_service(amount=200000, user_id=user.id)
        return Response(data=response['data'], status=response['status'])
