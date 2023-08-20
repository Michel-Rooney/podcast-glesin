import os

from django.shortcuts import get_object_or_404

from rest_framework.validators import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from . import models
from . import serializers
from . import utils
from .permissions import IsOwner, IsOwnerComment


class UserViewSets(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsOwner]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == 'list':
            return [IsAdminUser()]
        return permissions

    def perform_destroy(self, instance):
        if instance.avatar:
            os.remove(instance.avatar.path)
        return super().perform_destroy(instance)

    @action(['get'], False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        obj = get_object_or_404(models.User, id=request.user.id)
        serializers = self.get_serializer(
            instance=obj
        )
        return Response(serializers.data)


class CommentViewSets(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsOwnerComment, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

        params = self.request.query_params
        is_comment = params.get('comment', 'False')
        id_entity = self.request.POST.get('entity', '')

        if is_comment not in ['True', 'False']:
            raise ValidationError({
                'detail': 'Digite apenas True ou False'
            })

        entity = utils.get_podcast(id=id_entity)

        if is_comment == 'True':
            entity = utils.get_comment(id=id_entity)

        if not entity:
            raise ValidationError({
                'detail': 'Selecione um id válido.'
            })

        entity.comments.add(serializer.instance)
        return serializer

    @action(['get'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        obj = get_object_or_404(models.Comment, pk=pk)

        if request.user in obj.users_liked.all():
            raise ValidationError({
                'detail': 'Usuário já deu like.'
            })

        obj.likes += 1
        obj.users_liked.add(request.user.id)
        obj.users_disliked.remove(request.user.id)
        obj.save()

        return Response(status=status.HTTP_200_OK)

    @action(['get'], detail=True, permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        obj = get_object_or_404(models.Comment, pk=pk)

        if request.user in obj.users_disliked.all():
            raise ValidationError({
                'detail': 'Usuário já deu dislike.'
            })

        if not obj.likes <= 0:
            obj.likes -= 1
        obj.users_disliked.add(request.user.id)
        obj.users_liked.remove(request.user.id)
        obj.save()

        return Response(status=status.HTTP_200_OK)


class PodcastViewSets(ModelViewSet):
    queryset = models.Podcast.objects.all()
    serializer_class = serializers.PodcastSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method not in ['GET']:
            return [IsAdminUser()]
        return permissions

    def perform_destroy(self, instance):
        if instance.cover:
            os.remove(instance.cover.path)

        if instance.audio:
            os.remove(instance.audio.path)
        return super().perform_destroy(instance)

    @action(['get'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        obj = get_object_or_404(models.Podcast, pk=pk)

        if request.user in obj.users_liked.all():
            raise ValidationError({
                'detail': 'Usuário já deu like.'
            })

        obj.likes += 1
        obj.users_liked.add(request.user.id)
        obj.users_disliked.remove(request.user.id)
        obj.save()
        return Response(status=status.HTTP_200_OK)

    @action(['get'], detail=True, permission_classes=[IsAuthenticated])
    def dislike(self, request, pk=None):
        obj = get_object_or_404(models.Podcast, pk=pk)

        if request.user in obj.users_disliked.all():
            raise ValidationError({
                'detail': 'Usuário já deu dislike.'
            })

        if not obj.likes <= 0:
            obj.likes -= 1
        obj.users_disliked.add(request.user.id)
        obj.users_liked.remove(request.user.id)
        obj.save()

        return Response(status=status.HTTP_200_OK)
