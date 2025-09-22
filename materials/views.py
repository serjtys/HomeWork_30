from rest_framework import viewsets, generics, permissions
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .paginators import MaterialsPagination
from .services.stripe_service import create_stripe_product, create_stripe_price, create_stripe_session
from users.models import Payment
from django.http import HttpResponse


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):  # ← ВОТ ЭТОГО МЕТОДА НЕ ХВАТАЛО!
        if self.request.user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        old_updated_at = instance.updated_at

        instance = serializer.save()

        # Проверяем, что курс действительно обновился
        if instance.updated_at > old_updated_at:
            from .tasks import send_course_update_notification
            send_course_update_notification.delay(instance.id)

class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MaterialsPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsModerator, IsOwner]


class SubscriptionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({"error": "course_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if created:
            message = 'Подписка добавлена'
            return Response({"message": message}, status=status.HTTP_201_CREATED)
        else:
            subscription.delete()
            message = 'Подписка удалена'
            return Response({"message": message}, status=status.HTTP_200_OK)


class PaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({"error": "course_id обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        # Создаем продукт в Stripe
        product_id = create_stripe_product(
            name=course.title,
            description=course.description or "Оплата курса"
        )

        # Создаем цену
        # Берем цену directly из курса
        amount = course.price

        # Для теста можно было использовать хардкод:
        # amount = 1000

        price_id = create_stripe_price(product_id, amount)

        # Создаем сессию оплаты
        success_url = "http://localhost:8000/api/payment/success/"
        cancel_url = "http://localhost:8000/api/payment/cancel/"
        payment_url, session_id = create_stripe_session(price_id, success_url, cancel_url)

        # Сохраняем платеж в базе
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=amount,
            payment_method='transfer'
        )

        return Response({
            "payment_url": payment_url,
            "session_id": session_id,
            "payment_id": payment.id
        }, status=status.HTTP_201_CREATED)


class PaymentSuccessAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("✅ Оплата прошла успешно! Курс добавлен в ваш аккаунт.")

class PaymentCancelAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("❌ Оплата отменена. Вы можете попробовать снова.")