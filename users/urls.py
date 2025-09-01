from django.urls import path, include
from .views import UserUpdateAPIView, PaymentViewSet, UserRetrieveAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('', include(router.urls)),
]