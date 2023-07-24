from django.urls import path
from .views import BookView

urlpatterns = [
  path('book', BookView.as_view(), name="book_view"),
  path('book/<int:pk>', BookView.as_view(), name="book_view"),
]