from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserPostCreateFeed, PostMediaView, 
                    UserPostDeatilUpdateView, PostLikeViewSet,
                    PostCommentViewSet)

router = DefaultRouter()
router.register('like', PostLikeViewSet)
router.register('comment', PostCommentViewSet)
urlpatterns = router.urls

urlpatterns = [
    path('', UserPostCreateFeed.as_view(), name="user_post_view"),
    path('media/', PostMediaView.as_view(), name="user_media_view"),
    path('<int:pk>/', UserPostDeatilUpdateView.as_view(), name="user_media_view"),
    path('', include(router.urls)),

]