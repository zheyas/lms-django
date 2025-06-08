from rest_framework import generics, permissions, serializers
from users.models import User
from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer, UserProfileSerializer
from rest_framework.response import Response

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if self.kwargs['pk'] == str(self.request.user.pk):
                return [permissions.IsAuthenticated()]
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        # Человек может видеть чужой профиль только с публичными данными
        if self.request.user.pk == self.get_object().pk:
            return UserProfileSerializer
        else:
            class PublicProfileSerializer(serializers.ModelSerializer):
                class Meta:
                    model = User
                    fields = ('id', 'username')
            return PublicProfileSerializer
