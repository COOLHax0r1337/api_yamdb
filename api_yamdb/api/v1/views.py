from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminOrMe, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import UserSerializer

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review
from .filters import TitleFilter
from .serializers import (TitleReadSerializer,
                          TitleCreateSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          CommentSerializer
                          )


User = get_user_model()


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return TitleCreateSerializer
        return TitleReadSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug', url_name='category_slug'
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


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
