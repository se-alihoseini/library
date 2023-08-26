from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):

    def create_user(self, email, phone_number, first_name, last_name, password):

        if not email:
            raise ValueError("Users must have an email address")

        if not phone_number:
            raise ValueError("Users must have an phone_number")

        if not first_name:
            raise ValueError("Users must have an first_name")

        if not last_name:
            raise ValueError("Users must have an last_name")

        user = self.model(email=self.normalize_email(email), phone_number=phone_number,
                          first_name=first_name, last_name=last_name)
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, first_name, last_name, password):
        user = self.create_user(email, phone_number, first_name, last_name, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
