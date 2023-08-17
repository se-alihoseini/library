from django.urls import path
from user.views import user_pass_authentication, change_password, generate_password

app_name = 'user'
urlpatterns = [
    path('authentication/user_pass/', user_pass_authentication.UserPassAuthentication.as_view(),
         name='user_pass_authentication'),
    path('generate_password/', generate_password.GeneratePassword.as_view(), name='generate_password'),
    path('change_password/', change_password.ChangePassword.as_view(), name='change_password'),
]
