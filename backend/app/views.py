from .api_class import ApiView
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookView(ApiView):
   model = Book
   queryset = model.objects.select_related("category").all()
   objects = model.objects
   serializer_class = BookSerializer