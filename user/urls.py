from django.urls import path
from user.views import otp_authentication, send_otp, logout

app_name = 'user'
urlpatterns = [
    path('otp/send/', send_otp.SendOtp.as_view(), name='send_otp'),
    path('authentication/otp/', otp_authentication.OtpAuthentication.as_view(), name='otp_authentication'),
    path('logout/', logout.LogoutView.as_view(), name='logout'),
]

