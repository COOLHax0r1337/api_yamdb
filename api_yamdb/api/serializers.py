from django.shortcuts import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title, User

from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
    )

    class Meta:
        model = Comment
        read_only_fields = ('review', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='cannot post more'
            )
        ]
