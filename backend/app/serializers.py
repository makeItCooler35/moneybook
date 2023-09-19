'Сериэлайзеры'
from rest_framework import serializers
from .models import Book, Categories

class CategoriesSerializer(serializers.ModelSerializer):
    'Категории'
    class Meta:
        'Meta'
        model = Categories
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    'Книга с записями'
    class Meta:
        'Meta'
        model = Book
        fields = '__all__'
    category__name = serializers.CharField(source='category.name', read_only=True, default=None)
    time_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
