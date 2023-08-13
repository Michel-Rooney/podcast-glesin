from django.test import TestCase
from django.urls import reverse
from rest_framework import test
from app.models import User, Podcast, Comment


class AppBaseAPITest(test.APITestCase, TestCase):
    def create_superuser(
            self, username='UserAdmin', password='PassAdmin',
            email='testadmin@gmail.com'
    ):
        self.user = User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )
        return self.user

    def create_user(
            self, username='User', password='Pass',
            email='teste@gmail.com'
    ):
        self.user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return self.user

    def make_user_and_token(
            self, is_admin=False, username='UserToken', password='Pass'
    ):
        if is_admin:
            self.create_superuser(username, password)
        else:
            self.create_user(username, password)
        return self.get_jwt_access(username, password)

    def get_jwt_access(self, username='UserAdmin', password='PassAdmin'):
        data = {'username': username, 'password': password}

        url = reverse('app:token_obtain_pair')
        response = self.client.post(url, data=data)
        return response.data.get('access')

    def create_podcast(
            self, title='Title', audio='', authors=[]
    ):
        self.podcast = Podcast.objects.create(
            title=title,
            audio=''
        )
        if authors:
            for author in authors:
                self.podcast.authors.add(author)
        self.podcast.authors.add(self.user)
        return self.podcast

    def create_comment(
            self, content='Content', author=''
    ):
        if not author:
            author = self.user

        self.comment = Comment.objects.create(
            author=author,
            content=content
        )
        return self.comment
