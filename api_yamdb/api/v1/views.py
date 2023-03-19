from django.contrib.auth import get_user_model
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrMe
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrMe,)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    def get_object(self):
        if self.kwargs.get('username') != 'me':
            return super().get_object()
        return self.request.user

    def perform_destroy(self, instance):
        if (self.kwargs.get('username') == 'me'
                and self.request.method == 'DELETE'):
            self.http_method_not_allowed(self.request)
        super().perform_destroy(instance)
