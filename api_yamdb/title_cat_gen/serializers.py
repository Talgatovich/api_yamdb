from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from .models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
