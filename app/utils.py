from .models import Podcast, Comment


def get_podcast(**kwargs):
    podcast = Podcast.objects.filter(
        **kwargs
    ).prefetch_related(
        'users_liked', 'users_disliked', 'authors', 'comments'
    ).first()
    return podcast


def get_comment(**kwargs):
    comment = Comment.objects.filter(
        **kwargs
    ).select_related(
        'author'
    ).prefetch_related(
        'comments', 'users_liked', 'users_disliked'
    ).first()
    return comment
