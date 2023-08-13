from django.urls import reverse
from rest_framework import status
from .base import AppBaseAPITest


class UserViewAPITEST(AppBaseAPITest):
    """
                    ADMIN
    """
    def test_admin_app_user_api_list_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:user-api-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_admin_app_user_api_retrieve_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:user-api-detail', args=(1,))
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_admin_app_user_api_me_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:user-api-me')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.id, response.data['id'])

    def test_admin_app_user_api_create_passwords_dont_match(self):
        url = reverse('app:user-api-list')

        data = {
            'username': 'User',
            'password': 'Pass',
            'confirm_password': 'Invalid'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'As senhas não coicidem.', response.data['password'][0]
        )
        self.assertEqual(
            'As senhas não coicidem.', response.data['confirm_password'][0]
        )

    def test_admin_app_user_api_create_return_status_code_201_created(self):
        url = reverse('app:user-api-list')

        data = {
            'username': 'User',
            'password': 'Pass',
            'confirm_password': 'Pass'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data['username'], response.data['username'])

    def test_admin_app_user_api_update_passwords_dont_match(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:user-api-detail', args=(self.user.id,))

        data = {
            'first_name': 'Name',
            'password': 'Pass',
            'confirm_password': 'Invalid'
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'As senhas não coicidem.', response.data['password'][0]
        )
        self.assertEqual(
            'As senhas não coicidem.', response.data['confirm_password'][0]
        )

    def test_admin_app_user_api_update_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:user-api-detail', args=(self.user.id,))

        data = {
            'first_name': 'Name',
            'password': 'Pass',
            'confirm_password': 'Pass'
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['first_name'], response.data['first_name'])

    def test_admin_app_user_api_delete_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token(is_admin=True)}'
        url = reverse('app:user-api-detail', args=(self.user.id,))

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    """
                    User
    """
    def test_app_user_api_list_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:user-api-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_user_api_retrieve_return_status_code_403_forbidden(self):
        user = self.create_user('Up', 'Pass')
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:user-api-detail', args=(user.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_user_api_retrieve_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:user-api-detail', args=(1,))
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_app_user_api_me_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:user-api-me')
        response = self.client.get(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.user.id, response.data['id'])

    def test_app_user_api_create_passwords_dont_match(self):
        url = reverse('app:user-api-list')

        data = {
            'username': 'User',
            'password': 'Pass',
            'confirm_password': 'Invalid'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'As senhas não coicidem.', response.data['password'][0]
        )
        self.assertEqual(
            'As senhas não coicidem.', response.data['confirm_password'][0]
        )

    def test_app_user_api_create_return_status_code_201_created(self):
        url = reverse('app:user-api-list')

        data = {
            'username': 'User',
            'password': 'Pass',
            'confirm_password': 'Pass'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data['username'], response.data['username'])

    def test_app_user_api_update_passwords_dont_match(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:user-api-detail', args=(self.user.id,))

        data = {
            'first_name': 'Name',
            'password': 'Pass',
            'confirm_password': 'Invalid'
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            'As senhas não coicidem.', response.data['password'][0]
        )
        self.assertEqual(
            'As senhas não coicidem.', response.data['confirm_password'][0]
        )

    def test_app_user_api_update_return_status_code_403_forbidden(self):
        user = self.create_user()
        token = f'Bearer {self.make_user_and_token()}'

        url = reverse('app:user-api-detail', args=(user.id,))
        response = self.client.patch(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_user_api_update_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:user-api-detail', args=(self.user.id,))

        data = {
            'first_name': 'Name',
            'password': 'Pass',
            'confirm_password': 'Pass'
        }
        response = self.client.patch(url, HTTP_AUTHORIZATION=token, data=data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['first_name'], response.data['first_name'])

    def test_app_user_api_delete_return_status_code_403_forbidden(self):
        user = self.create_user()
        token = f'Bearer {self.make_user_and_token()}'

        url = reverse('app:user-api-detail', args=(user.id,))
        response = self.client.delete(url, HTTP_AUTHORIZATION=token)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_app_user_api_delete_return_status_code_200_success(self):
        token = f'Bearer {self.make_user_and_token()}'
        url = reverse('app:user-api-detail', args=(self.user.id,))

        response = self.client.delete(url, HTTP_AUTHORIZATION=token)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    """
                    UNAUTHORIZED
    """
    def test_not_logged_app_user_api_list_return_status_code_401(self):
        url = reverse('app:user-api-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_user_api_retrieve_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:user-api-detail', args=(user.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_user_api_me_return_status_code_401(self):
        url = reverse('app:user-api-me')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_user_api_create_return_status_code_201(self):
        url = reverse('app:user-api-list')

        data = {
            'username': 'User',
            'password': 'Pass',
            'confirm_password': 'Pass'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_not_logged_app_user_api_update_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:user-api-detail', args=(user.id,))
        response = self.client.patch(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_not_logged_app_user_api_delete_return_status_code_401(self):
        user = self.create_user()
        url = reverse('app:user-api-detail', args=(user.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
