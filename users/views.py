from rest_framework import generics, filters

from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PaymentSerializer  # <--- ваш путь до сериализатора
from .models import Payment

class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
    ordering_fields = ['date']
    ordering = ['-date']
