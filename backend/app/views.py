'''Здесь содержатся вьюшки для моделей'''
import base64
import uuid
import json
from datetime import datetime
import pytz
import pandas as pd
import numpy as np
from celery.result import AsyncResult
from django.http import HttpResponse
from django.conf import settings
from celery_app import app
from .api_class import ApiView
from .models import Book, Categories
from .serializers import BookSerializer, CategoriesSerializer

tz = pytz.utc

class CategoriesView(ApiView):
    'Описываем категории'
    model = Categories
    queryset = model.objects.all()
    objects = model.objects
    serializer_class = CategoriesSerializer
    default_sorting = ["-is_folder", "mcc"]

class BookView(ApiView):
    'Описываем свойства и методы работы с книгами (записями покупок)'
    model = Book
    categoties_model = Categories
    queryset = model.objects.select_related("category").all()
    objects = model.objects
    serializer_class = BookSerializer
    default_sorting = ["time_at"]

    @staticmethod
    @app.task(serializer='json')
    def upload_excel(data):
        'Подкачиваем записи в книгу из эксель от Тинькофф'
        view = BookView()
        file = base64.b64decode(data['file'])
        df_excel = pd.read_excel(file)
        strings = []
        batch_size = 500
        for item in df_excel.itertuples():
            if item[4] != 'OK':
                continue

            # сначала определим категорию
            mcc = 0 if np.isnan(item[11]) else item[11]
            category_id = view.categoties_model.objects.filter(mcc__exact=mcc, is_folder=False)[:1]
            if len(category_id) == 0:
                category_id = view.categoties_model.objects.create(
                    mcc=mcc, name=item[10], is_folder=False
                )
            else:
                category_id = category_id[0]

            strings.append(view.model(
                time_at=tz.localize(datetime.strptime(item[1], '%d.%m.%Y %H:%M:%S')),
                sum=item[5],
                bonus=0 if np.isnan(item[9]) else item[9],
                description=item[12],
                category=category_id
            ))

            if len(strings) == batch_size:
                view.model.objects.bulk_create(strings, batch_size=batch_size)
                strings = []

        view.model.objects.bulk_create(strings, batch_size=batch_size)
        return {'data': 'SUCCESS'}

    @staticmethod
    @app.task(serializer='json')
    def unload_excel(data):
        'Выгружаем данные из книги в эксель'
        # заглушка
        print(data)
        df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
                        index=['row 1', 'row 2'],
                        columns=['col 1', 'col 2'])

        path = f"{settings.REPORT_ROOT}/report_{str(uuid.uuid4())}.xlsx"
        df1.to_excel(path)

        return {
            'file': path,
            'headers': {
                'Content-Type': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                'Content-Disposition': 'attachment;'
            }
        }

    def fltr(self, qs_data, fltr):
        'Фильтр пользовательский'
        if fltr.get('categoryId'):
            # а вдруг это папка
            all_categories = CategoriesView.objects.raw('''
                WITH RECURSIVE tt AS(
                    SELECT
                        id
                    FROM app_categories 
                    WHERE id = %s AND is_folder = TRUE

                    UNION ALL

                    SELECT ac.id
                    FROM tt
                    JOIN app_categories ac ON ac.parent_id = tt.id
                )

                SELECT id FROM tt
            ''', [fltr['categoryId']])

            qs_data = qs_data.filter(category__in=[x.id for x in all_categories])

        if fltr.get('dateStart'):
            qs_data = qs_data.filter(time_at__gte=fltr['dateStart'])

        if fltr.get('dateEnd'):
            qs_data = qs_data.filter(time_at__lte=fltr['dateEnd'])

        if fltr.get('sum'):
            qs_data = qs_data.filter(sum=fltr['sum'])

        return qs_data

class JobsView(ApiView):
    'Описываем методы получения статуса фоновых работ и их результатов'
    def get(self, request, *args, **kwargs):
        job_id = request.query_params.get('jobId', None)
        async_res = {'status': None}
        if job_id:
            async_res = AsyncResult(job_id)

        is_end = 0 if async_res.status == 'PENDING' else 1
        job_result_return = is_end and int(request.query_params.get('get_result', 0))

        headers = {
        'Job-Id': job_id,
        'Job-End': is_end,
        'Job-Result-Return': job_result_return,
        'Access-Control-Expose-Headers': 'Job-Id, Job-End, Job-Result-Return'
        }

        if job_result_return:
            result = async_res.get()
            headers = headers | result.get('headers', {})
            if result.get('file', None):
                with open(result.get('file'), 'rb') as file:
                    return HttpResponse(content=file, headers=headers)
            else:
                return HttpResponse(content=result.get('data', {}), headers=headers)
        else:
            return HttpResponse(json.dumps({
                'status': async_res.status
            }), headers=headers)
