from django.urls import path, include
from .views import (UserUpdateAPIView, PaymentViewSet, UserRetrieveAPIView,
                   UserListAPIView, UserDestroyAPIView, UserRegistrationAPIView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('', include(router.urls)),
]