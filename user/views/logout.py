from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from user import services


import jwt


class LogoutView(APIView):

    def get(self, request):
        token = request.headers["Authorization"][7:]
        services.store_blocked_token(token=token, user_id=request.user.id)
        logout(request)
        return Response('your logout', status=status.HTTP_200_OK)
