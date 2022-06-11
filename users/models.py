from django.db import models

from core.models import TimeStampedModel

class User(TimeStampedModel):
    name         = models.CharField(max_length=50)
    email        = models.CharField(max_length=50)
    thumbnail    = models.CharField(max_length=300)
    introduction = models.TextField()
    subscription = models.ManyToManyField('self', symmetrical=False, through='Subscription')
    
    class Meta:
        db_table = 'users'

class SocialAccount(TimeStampedModel):
    social_account_id = models.CharField(max_length=300)
    name              = models.CharField(max_length=50)
    user              = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'social_accounts'


class Subscription(models.Model):
    subscriber      = models.ForeignKey(User, related_name='subscriber', on_delete=models.CASCADE)
    subscribed_user = models.ForeignKey(User, related_name='subscribed_user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'subscription'


