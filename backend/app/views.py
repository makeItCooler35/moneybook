from .api_class import ApiView
from .models import Book, Categories
from .serializers import BookSerializer, CategoriesSerializer
import pandas as pd
from datetime import datetime
import numpy as np

# Create your views here.
class CategoriesView(ApiView):
   model = Categories
   queryset = model.objects.all()
   objects = model.objects
   serializer_class = CategoriesSerializer
   default_sorting = "mcc"

class BookView(ApiView):
   model = Book
   categoties_model = Categories
   queryset = model.objects.select_related("category").all()
   objects = model.objects
   serializer_class = BookSerializer
   default_sorting = "time_at"

   def upload_excel(self, data):
      file = data['file']
      xl = pd.read_excel(file)
      for item in xl.itertuples():
         if item[4] == 'OK':
            # сначала определим категорию
            mcc = 0 if np.isnan(item[11]) else item[11]
            category_id = self.categoties_model.objects.filter(mcc__exact=mcc)[:1]
            if len(category_id) == 0:
               category_id = self.categoties_model.objects.create(
                  mcc=mcc,
                  name=item[10]
               )
            else:
               category_id = category_id[0]

            self.model.objects.create(
               time_at=datetime.strptime(item[1], '%d.%m.%Y %H:%M:%S'),
               sum=item[5],
               bonus=0 if np.isnan(item[9]) else item[9],
               description=item[12],
               category=category_id
            )
      return True