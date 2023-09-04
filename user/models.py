from user.manager import MyUserManager

import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):

    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    registry_date = models.DateField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    subscription_status = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')
    objects = MyUserManager()

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'

    @property
    def is_staff(self):
        return self.is_superuser


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_subscription')
    is_active = models.BooleanField(default=False)
    start_date_at = models.DateField(auto_now_add=True)
    end_date_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-Subscription'


class OtpCode(models.Model):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, related_name='otp_code_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_otp(cls, user):
        code = ''.join(random.choice(string.digits) for i in range(4))
        code_obj = OtpCode.objects.create(code=code, user=user)
        return code_obj

    @classmethod
    def check_otp(cls, code, user):
        otp_code = OtpCode.objects.get(code=code, user=user)
        if otp_code is not None:
            OtpCode.objects.filter(user=user).delete()
            return True
        else:
            return False


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('su', 'successful'),
        ('un', 'unsuccessful')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_transaction')
    transaction_code = models.CharField(max_length=20)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    cost = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.created_at}'
