from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=255, unique=True)
    first_name = models.CharField('first name', max_length=255, blank=True)
    last_name = models.CharField('last name', max_length=255, blank=True)
    is_staff = models.BooleanField(
        'staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(
        'active', default=False,
        help_text=('Designates whether this user should be treated as '
                   'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    confirm_key = models.CharField(max_length=40, unique=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        ordering = ['email']

    def save(self, *args, **kwargs):
        if not self.confirm_key:
            while True:
                confirm_key = get_random_string(length=25)
                exists = self.__class__.objects.filter(
                    confirm_key=confirm_key).exists()
                if not exists:
                    self.confirm_key = confirm_key
                    break

        return super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def send_confirm_email(self):
        confirm_url = '{}{}?code={}'.format(
            settings.EMAIL_HOST,
            reverse_lazy('users:confirm'),
            self.confirm_key,
        )

        send_mail(
            'Confirm your Email Address',
            confirm_url,
            settings.EMAIL_ADMIN,
            [self.email])

        return True
