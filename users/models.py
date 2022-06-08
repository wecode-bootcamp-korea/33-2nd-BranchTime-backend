from django.db import models

from core.models import TimeStampedModel

class User(TimeStampedModel):
    name         = models.CharField(max_length=50)
    email        = models.CharField(max_length=50)
    thumbnail    = models.CharField(max_length=300)
    introduction = models.TextField()
    
    class Meta:
        db_table = 'users'

class SocialAccount(TimeStampedModel):
    social_acccunt_id = models.CharField(max_length=300)
    name              = models.CharField(max_length=50)
    social_login      = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'social_accounts'

