from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views


app_name = 'app'

urlpatterns_jwt = [
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
]

router = DefaultRouter()
router.register('api/users', views.UserViewSets, basename='user-api')
router.register('api/comment', views.CommentViewSets, basename='comment-api')
router.register('api/podcast', views.PodcastViewSets, basename='podcast-api')

print(router.urls)

urlpatterns = router.urls
urlpatterns += urlpatterns_jwt
