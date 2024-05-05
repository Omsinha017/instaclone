from django.urls import path
from . views import create_user, user_list, UserProfileDetail, UserNetworkEdge
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('add/', create_user, name="user_main_views"),
    path('login/', TokenObtainPairView.as_view(), name="token_obtain_pair_views"),
    path('list/', user_list, name="user_list_views"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('<int:pk>/', UserProfileDetail.as_view(), name='get_user_profile'),
    path('edge/', UserNetworkEdge.as_view(), name='network_edge'),

]