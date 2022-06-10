from django.db import models

from core.models import TimeStampedModel

from authors.models import Author
from users.models import User

class Book(TimeStampedModel):
    title  = models.CharField(max_length=45)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    class Meta:
        db_table = "books"

class Work(TimeStampedModel):
    introduction        = models.TextField()
    title               = models.CharField(max_length=45)
    recommended_title   = models.CharField(max_length=45)
    recommended_content = models.TextField()
    author              = models.ForeignKey(Author, on_delete = models.CASCADE)
    
    class Meta:
        db_table = "works"

class WorkLike(models.Model):
    work = models.ForeignKey(Work, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    class Meta:
        db_table = "work_likes"

class Post(TimeStampedModel):
    title           = models.CharField(max_length=150)
    sub_title       = models.CharField(max_length=150)
    thumbnail_image = models.CharField(max_length=150)
    content         = models.TextField()
    reading_time    = models.TimeField()
    work            = models.ForeignKey(Work, on_delete = models.CASCADE, null=True)
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    subcategory     = models.ForeignKey('SubCategory', on_delete = models.CASCADE)

    class Meta:
        db_table = "posts"

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    class Meta:
        db_table = "post_likes"

class Comment(TimeStampedModel):
    image   = models.CharField(max_length=150)
    content = models.TextField()
    post    = models.ForeignKey(Post, on_delete = models.CASCADE)
    user    = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        db_table = "comments"

class MainCategory(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "maincategories"

class SubCategory(models.Model):
    name         = models.CharField(max_length=45)
    maincategory = models.ForeignKey(MainCategory, on_delete = models.CASCADE)

    class Meta:
        db_table = "subcategories"