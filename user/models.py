import random
import string

from user.manager import MyUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.shortcuts import get_object_or_404
from django.core.validators import ValidationError


class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('ac', 'active'),
        ('da', 'de_active'),
        ('bl', 'block'),
        ('de', 'delete'),
    ]
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='', blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default='da')
    change_password = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')
    objects = MyUserManager()

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'

    @property
    def is_staff(self):
        return self.is_superuser

    def clean(self):
        try:
            user = User.objects.get(is_superuser=True)
        except User.DoesNotExist:
            user = None
        if user is not None:
            raise ValidationError(
                {'is_superuser': "there is a super user"})

    def check_otp(self, code):
        try:
            OtpCode.objects.filter(user=self, code=code)
            OtpCode.objects.filter(user=self).delete()
            return True
        except OtpCode.DoesNotExist:
            return False

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(12))
        print(password)

    @classmethod
    def get_user(cls, email_phone):
        if '@' in email_phone:
            user = get_object_or_404(cls, email=email_phone)
        else:
            user = get_object_or_404(cls, phone_number=email_phone)
        return user

    @classmethod
    def check_user_pass(self, data):
        email_phone = data['email_phone']
        password = data['password']
        user = User.get_user(email_phone)
        if user is None:
            return False
        else:
            if user.check_password(password):
                OtpCode.send_otp(user=self)
                return True
            else:
                return False


class OtpCode(models.Model):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, related_name='otp_code_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def send_otp(cls, user):
        code = ''.join(random.choice(string.digits) for i in range(5))
        OtpCode.objects.create(code=code, user=user)
        print(code)
