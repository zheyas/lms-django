from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from .models import Payment
from .serializers import PaymentSerializer  # <--- ваш путь до сериализатора


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["date"]
    ordering = ["-date"]


from rest_framework import generics, permissions, viewsets

from .models import User
from .serializers import (
    UserProfileSerializer,
    UserPublicSerializer,
    UserRegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            # Если пользователь смотрит чужой профиль
            if self.kwargs["pk"] and int(self.kwargs["pk"]) != self.request.user.pk:
                return UserPublicSerializer
        return UserProfileSerializer

    def get_permissions(self):
        # Разрешаем редактировать только свой профиль
        if self.action in ("update", "partial_update", "destroy"):
            user = self.get_object()
            if self.request.user != user:
                self.permission_denied(self.request)
        return super().get_permissions()
