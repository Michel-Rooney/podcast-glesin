from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatar/%Y/%m/%d/', blank=True, null=True
    )

    def __str__(self):
        return self.username


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comments = models.ManyToManyField('self', blank=True)
    likes = models.IntegerField(blank=True, null=True, default=0)
    users_liked = models.ManyToManyField(
        User, related_name='comment_liked', blank=True)
    users_disliked = models.ManyToManyField(
        User, related_name='comment_disliked', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def list_comments(self):
        return self.comments.all()[1:]

    def __str__(self) -> str:
        return self.content[0:50]


class Podcast(models.Model):
    cover = models.ImageField(
        upload_to='cover/%Y/%m/%d/', blank=True, null=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    audio = models.FileField(upload_to='audio/%Y/%m/%d/')
    likes = models.IntegerField(blank=True, null=True, default=0)
    users_liked = models.ManyToManyField(
        User, related_name='podcast_liked', blank=True)
    users_disliked = models.ManyToManyField(
        User, related_name='podcast_disliked', blank=True)
    authors = models.ManyToManyField(User)
    comments = models.ManyToManyField(Comment, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
