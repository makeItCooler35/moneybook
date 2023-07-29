from django.urls import path
from .views import BookView, CategoriesView

urlpatterns = [
  path('book', BookView.as_view(), name="book_view"),
  path('book/<int:pk>', BookView.as_view(), name="book_view"),
  path('categories', CategoriesView.as_view(), name="categories_view"),
  path('categories/<int:pk>', CategoriesView.as_view(), name="categories_view"),
]