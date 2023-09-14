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
from django.conf import settings
import uuid

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
    return {'data': 'SUCCESS'}

  @staticmethod
  @app.task(serializer='json')
  def unload_excel(data):
    # заглушка
    df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
                      index=['row 1', 'row 2'],
                      columns=['col 1', 'col 2'])

    path = "{report_root}/report_{uuid}.xlsx".format(report_root=settings.REPORT_ROOT, uuid=str(uuid.uuid4()))
    df1.to_excel(path)

    return {
      'file': path,
      'headers': {
        'Content-Type': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        'Content-Disposition': 'attachment;'
      }
    }

class JobsView(ApiView):
  def get(self, request, *args, **kwargs):
    job_id = request.query_params.get('jobId', None)
    asyncRes = {'status': None}
    if job_id:
      asyncRes = AsyncResult(job_id)

    is_end = 0 if asyncRes.status == 'PENDING' else 1
    job_result_return = is_end and int(request.query_params.get('get_result', 0))
    
    headers = {
      'Job-Id': job_id,
      'Job-End': is_end,
      'Job-Result-Return': job_result_return,
      'Access-Control-Expose-Headers': 'Job-Id, Job-End, Job-Result-Return'
    }

    if job_result_return:
      result = asyncRes.get()
      headers = headers | result.get('headers', {})
      if(result.get('file', None)):
        with open(result.get('file'), 'rb') as f:
          return HttpResponse(content=f, headers=headers)
      else:
        return HttpResponse(content=result.get('data', {}), headers=headers)
    else:
      return HttpResponse(json.dumps({
        'status': asyncRes.status
      }), headers=headers)