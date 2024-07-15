from django.urls import path

from apps.users.views import UserRegistrationAPIView, UserDetailAPIView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('user-detail/', UserDetailAPIView.as_view(), name='user-detail'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout')
]
