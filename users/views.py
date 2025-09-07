from rest_framework import generics, viewsets
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PaymentFilter


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']