import os
from PIL import Image
from collections import defaultdict

from django.conf import settings

from rest_framework import serializers
from rest_framework.validators import ValidationError

from . import models
from .utils import get_podcast


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(
        write_only=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = defaultdict(list)

    class Meta:
        model = models.User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'password', 'confirm_password', 'avatar',
        ]

    def save(self, **kwargs):
        password = self.validated_data.get('password')
        self.validated_data.pop('confirm_password', '')

        user = super().save(**kwargs)
        user.set_password(password)

        if user.avatar:
            self.resize_image(user.avatar, 170)

        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            self.messages['password'].append('As senhas não coicidem.')
            self.messages['confirm_password'].append('As senhas não coicidem.')

        if self.messages:
            raise ValidationError(self.messages)

        return super().validate(attrs)

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_URL, image.path)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = [
            'id', 'author', 'content', 'likes', 'users_liked',
            'users_disliked', 'comments', 'creation_date'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        obj = models.Comment.objects.get(id=instance.id)
        data['author'] = UserSerializer(instance.author).data
        data['comments'] = CommentSerializer(
            obj.list_comments(), many=True
        ).data
        return data


class PodcastSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = defaultdict(list)

    class Meta:
        model = models.Podcast
        fields = [
            'id', 'cover', 'title', 'description', 'audio',
            'likes', 'users_liked', 'users_disliked',
            'authors', 'comments', 'creation_date'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['authors'] = UserSerializer(instance.authors, many=True).data
        data['comments'] = CommentSerializer(instance.comments, many=True).data
        return data

    def save(self, **kwargs):
        podcast = super().save(**kwargs)

        if podcast.cover:
            self.resize_image(podcast.cover, 1080)

        podcast.save()
        return podcast

    def validate(self, attrs):
        if self.messages:
            raise ValidationError(self.messages)
        return super().validate(attrs)

    def validate_title(self, attr):
        exist = get_podcast(title=attr)
        if exist:
            if self.instance != exist:
                self.messages['title'].append('Esse titulo já está em uso.')
        return attr

    def validate_audio(self, attr):
        _, extension = os.path.splitext(str(attr))

        if extension != '.mp3':
            self.messages['audio'].append(
                'Formato de arquivo inválido. Somente arquivos .mp3 permitidos'
            )
        return attr

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_URL, image.path)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )
