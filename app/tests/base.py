import os
import shutil
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework import test
from app.models import User, Podcast, Comment


class AppBaseAPITest(test.APITestCase, TestCase):
    def create_superuser(
            self, username='UserAdmin', password='PassAdmin',
            email='testadmin@gmail.com'
    ):
        source_path = settings.BASE_DIR / 'media/cover/test/Pingu.png'
        avatar_path = settings.BASE_DIR / 'media/cover/test/Pingu_avatar.png'
        shutil.copy(source_path, avatar_path)

        self.user = User.objects.create_superuser(
            username=username,
            password=password,
            email=email,
            avatar=os.path.join(avatar_path),
        )
        return self.user

    def create_user(
            self, username='User', password='Pass',
            email='teste@gmail.com'
    ):
        source_path = settings.BASE_DIR / 'media/cover/test/Pingu.png'
        avatar_path = settings.BASE_DIR / 'media/cover/test/Pingu_avatar.png'
        shutil.copy(source_path, avatar_path)

        self.user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            avatar=os.path.join(avatar_path),
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
        source_path = settings.BASE_DIR / 'media/cover/test/Pingu.png'
        cover_path = settings.BASE_DIR / 'media/cover/test/Pingu_test.png'
        shutil.copy(source_path, cover_path)

        source_path = settings.BASE_DIR / 'media/audio/test/LosT.mp3'
        audio_path = settings.BASE_DIR / 'media/audio/test/LosT_test.mp3'
        shutil.copy(source_path, audio_path)

        self.podcast = Podcast.objects.create(
            cover=os.path.join(cover_path),
            title=title,
            audio=os.path.join(audio_path),
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
