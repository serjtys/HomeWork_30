import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    course = django_filters.CharFilter(field_name='course__title', lookup_expr='icontains')
    course_id = django_filters.NumberFilter(field_name='course__id')
    lesson = django_filters.CharFilter(field_name='lesson__title', lookup_expr='icontains')
    lesson_id = django_filters.NumberFilter(field_name='lesson__id')
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ['course', 'course_id', 'lesson', 'lesson_id', 'payment_method']