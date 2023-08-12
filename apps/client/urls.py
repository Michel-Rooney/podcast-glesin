from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import views


router = DefaultRouter()
router.register('api/users', views.UserViewSets, basename='user-api')
router.register('api/comment', views.CommentViewSets, basename='comment-api')
router.register('api/podcast', views.PodcastViewSets, basename='podcast-api')

# JWT
router.register(
    'api/token/', TokenObtainPairView, basename='token_obtain_pair'
)
router.register(
    'api/token/refresh/', TokenRefreshView, basename='token_refresh'
)
router.register('api/token/verify/', TokenVerifyView, basename='token_verify')

urlpatterns = router.urls
