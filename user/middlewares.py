from library import settings
from django.core.exceptions import PermissionDenied
from django.urls import reverse
import redis


LOGIN_EXEMPT_URLS = [
    reverse('user:send_otp'),
    reverse('user:otp_authentication'),
]


class BlockTokensCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path not in LOGIN_EXEMPT_URLS:
            r = redis.Redis(host=settings.REDIS_CONFIG["host"], port=settings.REDIS_CONFIG["port"])
            token = request.headers["Authorization"][7:]
            if r.exists(token):
                raise PermissionDenied()
        response = self.get_response(request)
        return response
