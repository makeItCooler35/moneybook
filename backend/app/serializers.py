from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = '__all__'
  category_name = serializers.CharField(source='category.name', read_only=True, default=None)
  time_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
