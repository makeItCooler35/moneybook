from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
  category_name = serializers.CharField(source='category.name', read_only=True, default=None)
  class Meta:
    model = Book
    fields = '__all__'