from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg

from reviews.models import Category, Genre, Title
from .serializers import TitleReadSerializer, TitleCreateSerializer, CategorySerializer, GenreSerializer
from .filters import TitleFilter


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    )
    serializer_class = TitleReadSerializer
    filterset_class = TitleFilter

    # permission_classes =

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleReadSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes =
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes =
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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
