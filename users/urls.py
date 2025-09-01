from django.urls import path
from .views import UserUpdateAPIView

urlpatterns = [
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
]