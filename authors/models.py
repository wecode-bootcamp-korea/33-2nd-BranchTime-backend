from django.db import models

from core.models import TimeStampedModel
from users.models import User

class Author(TimeStampedModel):
    introduction = models.TextField()
    career       = models.TextField()
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    subcategory  = models.ForeignKey('contents.SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'authors'

class Site(models.Model):
    site_url = models.CharField(max_length=300)
    author   = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sites'

class InterestedAuthor(models.Model):
    user   = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = 'interested_authors'

class ProposalObject(models.Model):
    name = models.CharField(max_length=30)        

    class Meta:
        db_table = 'proposal_objects'

class Proposal(TimeStampedModel): 
    sender_email    = models.CharField(max_length=50)        
    content         = models.TextField()
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    author          = models.ForeignKey(Author, on_delete=models.CASCADE)
    proposal_object = models.ForeignKey(ProposalObject, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'proposals'