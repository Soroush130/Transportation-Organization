from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from datetime import datetime

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError('The Phone must be set')

        user = self.model(phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone=phone,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    ROLE = (
        ('factory', 'Factory'),
        ('freight', 'Freight'),
        ('driver', 'Driver'),
    )
    phone = models.CharField(verbose_name='Phone-Number', max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=ROLE, default='factory')
    username = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    data_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.is_staff


class FactoryMember(models.Model):
    factory = models.ForeignKey(User, on_delete=models.CASCADE, related_name='factories')
    freight = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freight_companies')

    def __str__(self):
        return f'{self.freight} is a member {self.factory}'


class OtpCode(models.Model):
    phone = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=5)
    is_valid = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.otp_code