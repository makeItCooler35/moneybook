from .api_class import ApiView
from .models import Book, Categories
from .serializers import BookSerializer, CategoriesSerializer

# Create your views here.
class CategoriesView(ApiView):
   model = Categories
   queryset = model.objects.all()
   objects = model.objects
   serializer_class = CategoriesSerializer

class BookView(ApiView):
   model = Book
   queryset = model.objects.select_related("category").all()
   objects = model.objects
   serializer_class = BookSerializer