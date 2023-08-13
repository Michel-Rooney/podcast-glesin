from django.urls import reverse
from rest_framework import status
from .base import AppBaseAPITest
from app.models import Comment


class UserViewAPITEST(AppBaseAPITest):
    """
                    ADMIN
    """
    def test_admin_app_comment_api_list_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:comment-api-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_admin_app_comment_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        comment = self.create_comment()
        url = reverse('app:comment-api-detail', args=(comment.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_admin_app_comment_api_create_return_status_code_201_created(self):
        url = reverse('app:comment-api-list')
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()

        data = {
            'content': 'Content',
            'author': self.user.id,
            'entity': podcast.id
        }
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data['content'], response.data['content'])

    def test_admin_app_comment_api_update_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        podcast = self.create_podcast()
        comment = self.create_comment()
        url = reverse('app:comment-api-detail', args=(comment.id, ))

        data = {
            'content': 'New Content',
            'author': self.user.id,
            'entity': podcast.id
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['content'], response.data['content'])

    def test_admin_app_comment_api_delete_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        comment = self.create_comment()
        url = reverse('app:comment-api-detail', args=(comment.id,))

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_admin_app_comment_api_like_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        comment = self.create_comment()
        url = reverse('app:comment-api-like', args=(comment.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(1, comment.likes)

    def test_admin_app_comment_api_like_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        comment = self.create_comment()
        url = reverse('app:comment-api-like', args=(comment.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu like.', response.data['detail'])

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(1, comment.likes)

    def test_admin_app_comment_api_dislike_return_status_code_200_success(self):  # noqa: E501
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        comment = self.create_comment()
        url = reverse('app:comment-api-dislike', args=(comment.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(0, comment.likes)

    def test_admin_app_comment_api_dislike_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        comment = self.create_comment()
        url = reverse('app:comment-api-dislike', args=(comment.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu dislike.', response.data['detail'])

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(0, comment.likes)

    """
                    User
    """
    def test_app_comment_api_list_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:comment-api-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_app_comment_api_retrieve_return_status_code_200_success(self):  # noqa: E501
        token = f'Bearer {self.make_user_and_token()}'
        comment = self.create_comment()
        url = reverse('app:comment-api-detail', args=(comment.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_app_comment_api_create_return_status_code_201_created(self):
        url = reverse('app:comment-api-list')
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()

        data = {
            'content': 'Content',
            'author': self.user.id,
            'entity': podcast.id
        }
        response = self.client.post(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data['content'], response.data['content'])

    def test_app_comment_api_update_return_status_code_403(self):
        token = f'Bearer {self.make_user_and_token()}'
        user = self.create_user('Up')
        comment = self.create_comment(author=user)
        url = reverse('app:comment-api-detail', args=(comment.id, ))

        response = self.client.patch(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_comment_api_update_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        podcast = self.create_podcast()
        comment = self.create_comment()
        url = reverse('app:comment-api-detail', args=(comment.id, ))

        data = {
            'content': 'New Content',
            'author': self.user.id,
            'entity': podcast.id
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['content'], response.data['content'])

    def test_app_comment_api_delete_return_status_code_403(self):
        token = f'Bearer {self.make_user_and_token()}'
        user = self.create_user()
        comment = self.create_comment(author=user)
        url = reverse('app:comment-api-detail', args=(comment.id,))

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_comment_api_delete_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        comment = self.create_comment()
        url = reverse('app:comment-api-detail', args=(comment.id,))

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_app_comment_api_like_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        comment = self.create_comment()
        url = reverse('app:comment-api-like', args=(comment.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(1, comment.likes)

    def test_app_comment_api_like_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token()}'
        comment = self.create_comment()
        url = reverse('app:comment-api-like', args=(comment.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu like.', response.data['detail'])

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(1, comment.likes)

    def test_app_comment_api_dislike_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        comment = self.create_comment()
        url = reverse('app:comment-api-dislike', args=(comment.id, ))

        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(0, comment.likes)

    def test_app_comment_api_dislike_return_status_code_400(self):
        token = f'Bearer {self.make_user_and_token()}'
        comment = self.create_comment()
        url = reverse('app:comment-api-dislike', args=(comment.id, ))

        self.client.get(url, HTTP_AUTHORIZATION=token)
        response = self.client.get(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Usuário já deu dislike.', response.data['detail'])

        comment = Comment.objects.get(id=comment.id)
        self.assertEqual(0, comment.likes)

    """
                    UNAUTHORIZED
    """
    def test_not_logged_app_comment_api_list_return_status_code_401(self):
        url = reverse('app:comment-api-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_comment_api_retrieve_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:comment-api-detail', args=(user.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_comment_api_create_return_status_code_401(self):
        url = reverse('app:comment-api-list')
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_comment_api_update_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:comment-api-detail', args=(user.id,))
        response = self.client.patch(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_comment_api_delete_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:comment-api-detail', args=(user.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_comment_api_like_return_status_code_401(self):
        user = self.create_user()
        podcast = self.create_comment(author=user)
        url = reverse('app:podcast-api-like', args=(podcast.id, ))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_comment_api_dislike_return_status_code_401(self):
        user = self.create_user()
        podcast = self.create_comment(author=user)
        url = reverse('app:podcast-api-dislike', args=(podcast.id, ))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
