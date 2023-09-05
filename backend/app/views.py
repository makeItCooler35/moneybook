from django.views import View
from .api_class import ApiView
from .models import Book, Categories
from .serializers import BookSerializer, CategoriesSerializer
import pandas as pd, numpy as np, base64
from django.http import HttpResponse
import json
import pytz
from datetime import datetime
from celery.result import AsyncResult
from celery_app import app

tz = pytz.utc

class CategoriesView(ApiView):
  model = Categories
  queryset = model.objects.all()
  objects = model.objects
  serializer_class = CategoriesSerializer
  default_sorting = ["-is_folder", "mcc"]

class BookView(ApiView):
  model = Book
  categoties_model = Categories
  queryset = model.objects.select_related("category").all()
  objects = model.objects
  serializer_class = BookSerializer
  default_sorting = ["time_at"]

  @staticmethod
  @app.task(serializer='json')
  def upload_excel(data):
    view = BookView()
    file = base64.b64decode(data['file'])
    xl = pd.read_excel(file)
    ls = []
    batch_size = 500
    for item in xl.itertuples():
      if item[4] != 'OK':
        continue

      # сначала определим категорию
      mcc = 0 if np.isnan(item[11]) else item[11]
      category_id = view.categoties_model.objects.filter(mcc__exact=mcc, is_folder=False)[:1]
      if len(category_id) == 0:
        category_id = view.categoties_model.objects.create(
          mcc=mcc,
          name=item[10],
          is_folder=False
        )
      else:
        category_id = category_id[0]
      
      ls.append(view.model(
        time_at=tz.localize(datetime.strptime(item[1], '%d.%m.%Y %H:%M:%S')),
        sum=item[5],
        bonus=0 if np.isnan(item[9]) else item[9],
        description=item[12],
        category=category_id
      ))

      if(len(ls) == batch_size):
        view.model.objects.bulk_create(ls, batch_size=batch_size)
        ls = []
  
    view.model.objects.bulk_create(ls, batch_size=batch_size)
    return True

class JobsView(ApiView):
  def get(self, request, *args, **kwargs):
    jobId = request.query_params.get('jobId', None)
    asyncRes = {'status': None}
    if jobId:
      asyncRes = AsyncResult(jobId)

    return HttpResponse(json.dumps({
      'status': asyncRes.status,
      'jobId': jobId,
      'end': False if asyncRes.status == 'PENDING' else True
    }))