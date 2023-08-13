import os
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from .base import AppBaseAPITest
from app.models import Podcast


class UserViewAPITEST(AppBaseAPITest):
    """
                    ADMIN
    """
    def test_admin_app_podcast_api_list_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:podcast-api-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_admin_app_podcast_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-detail', args=(podcast.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_admin_app_podcast_api_create_invalid_audio(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:podcast-api-list')

        data = {
            'title': 'Title',
            'audio': '',
            'authors': 1
        }
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)
        self.podcast = response.data

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn(
            (
             'O dado submetido não é um arquivo. Certifique-se do '
             'tipo de codificação no formulário.'
            ),
            response.data['audio'][0]
        )

    def test_admin_app_podcast_api_create_audio_format_invalid(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:podcast-api-list')

        data = {
            'title': 'Title',
            'audio': open(settings.BASE_DIR / 'requirements.txt', 'rb'),
            'authors': 1
        }
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn(
            'Formato de arquivo inválido. Somente arquivos .mp3 permitidos',
            response.data['audio'][0]
        )

    def test_admin_app_podcast_api_create_title_exist(self):
        TITLE = 'Userd Titulo'
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        self.create_podcast(TITLE)
        url = reverse('app:podcast-api-list')

        data = {
            'title': TITLE,
            'audio': open(
                settings.BASE_DIR / 'media/audio/teste/LosT.mp3', 'rb'
            ),
            'authors': self.user.id
        }
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn(
            'Esse titulo já está em uso.',
            response.data['title'][0]
        )

    def test_admin_app_podcast_api_create_return_status_code_201_created(self):
        url = reverse('app:podcast-api-list')
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'

        data = {
            'title': 'Title',
            'audio': open(
                settings.BASE_DIR / 'media/audio/teste/LosT.mp3', 'rb'
            ),
            'authors': self.user.id
        }
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data['title'], response.data['title'])

        podcast = Podcast.objects.get(id=response.data['id'])
        os.remove(podcast.audio.path)

    def test_admin_app_podcast_api_update_title_exist(self):
        TITLE = 'Userd Titulo'
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        self.create_podcast(TITLE)
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-detail', args=(podcast.id, ))

        data = {
            'title': TITLE,
            'audio': open(
                settings.BASE_DIR / 'media/audio/teste/LosT.mp3', 'rb'
            ),
            'authors': self.user.id
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertIn(
            'Esse titulo já está em uso.',
            response.data['title'][0]
        )

    def test_admin_app_podcast_api_update_return_status_code_200_success(self):
        TITLE = 'Titulo'
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast(TITLE)
        url = reverse('app:podcast-api-detail', args=(podcast.id,))

        data = {
            'title': TITLE,
            'audio': open(
                settings.BASE_DIR / 'media/audio/teste/LosT.mp3', 'rb'
            ),
            'authors': self.user.id
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['title'], response.data['title'])

        podcast = Podcast.objects.get(id=response.data['id'])
        os.remove(podcast.audio.path)

    def test_admin_app_podcast_api_delete_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-detail', args=(podcast.id,))

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_admin_app_podcast_api_like_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-like', args=(podcast.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(1, podcast.likes)

    def test_admin_app_podcast_api_like_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-like', args=(podcast.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu like.', response.data['detail'])

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(1, podcast.likes)

    def test_admin_app_podcast_api_dislike_return_status_code_200_success(self):   # noqa: E501
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-dislike', args=(podcast.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(0, podcast.likes)

    def test_admin_app_podcast_api_dislike_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-dislike', args=(podcast.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu dislike.', response.data['detail'])

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(0, podcast.likes)

    """
                    User
    """
    def test_app_podcast_api_list_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:podcast-api-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_app_podcast_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-detail', args=(podcast.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_app_podcast_api_create_return_status_code_403_forbidden(self):
        url = reverse('app:podcast-api-list')
        token = f'Bearer {self.make_user_and_token()}'
        response = self.client.post(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_podcast_api_update_return_status_code_403_forbidden(self):
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-detail', args=(podcast.id,))

        response = self.client.patch(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_podcast_api_delete_return_status_code_403_forbidden(self):
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-detail', args=(podcast.id,))

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_podcast_api_like_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-like', args=(podcast.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(1, podcast.likes)

    def test_app_podcast_api_like_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-like', args=(podcast.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu like.', response.data['detail'])

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(1, podcast.likes)

    def test_app_podcast_api_dislike_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-dislike', args=(podcast.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(0, podcast.likes)

    def test_app_podcast_api_dislike_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        url = reverse('app:podcast-api-dislike', args=(podcast.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu dislike.', response.data['detail'])

        podcast = Podcast.objects.get(id=podcast.id)
        self.assertEqual(0, podcast.likes)

    """
                    UNAUTHORIZED
    """
    def test_not_logged_app_podcast_api_list_return_status_code_401(self):
        url = reverse('app:podcast-api-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_podcast_api_retrieve_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:podcast-api-detail', args=(user.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_podcast_api_create_return_status_code_401(self):
        url = reverse('app:podcast-api-list')
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_podcast_api_update_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:podcast-api-detail', args=(user.id,))
        response = self.client.patch(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_podcast_api_delete_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:podcast-api-detail', args=(user.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_podcast_api_like_return_status_code_401(self):
        user = self.create_user()
        podcast = self.create_podcast(user)
        url = reverse('app:podcast-api-like', args=(podcast.id, ))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_podcast_api_dislike_return_status_code_401(self):
        user = self.create_user()
        podcast = self.create_podcast(user)
        url = reverse('app:podcast-api-dislike', args=(podcast.id, ))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
