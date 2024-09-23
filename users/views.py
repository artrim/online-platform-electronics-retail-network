from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.paginators import UserPaginator
from users.permissions import IsUsers
from users.serializers import UserSerializer, UserListSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
            self.serializer_class = UserSerializer
        if self.action in ['list']:
            self.permission_classes = [IsAuthenticated]
            self.serializer_class = UserListSerializer
        if self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated, IsUsers]
            self.serializer_class = UserSerializer
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsUsers]
            self.serializer_class = UserSerializer
        return super().get_permissions()

    def perform_create(self, serializer):
        instance = serializer.save(is_active=True)
        instance.set_password(instance.password)
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
