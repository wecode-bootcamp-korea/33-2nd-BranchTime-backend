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
    social_account_id = models.CharField(max_length=300)
    name              = models.CharField(max_length=50)
    uesr              = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'social_accounts'

