from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

class User(AbstractBaseUser):
    referral_code = models.CharField(max_length=50, unique=True, blank=True)

class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='referred_users', null=True)
    registration_timestamp = models.DateTimeField(default=timezone.now)
