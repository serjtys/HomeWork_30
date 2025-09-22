from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CourseViewSet, LessonListAPIView, LessonCreateAPIView,
                   LessonRetrieveAPIView, LessonUpdateAPIView, LessonDestroyAPIView,
                    SubscriptionAPIView, PaymentAPIView, PaymentSuccessAPIView, PaymentCancelAPIView)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
    path('payment/', PaymentAPIView.as_view(), name='payment'),
    path('payment/', PaymentAPIView.as_view(), name='payment'),
    path('payment/success/', PaymentSuccessAPIView.as_view(), name='payment-success'),
    path('payment/cancel/', PaymentCancelAPIView.as_view(), name='payment-cancel'),
]