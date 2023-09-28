'Здесь содержится общий класс для ответов'

import json
import math
import base64
from rest_framework.response import Response
from rest_framework import generics
from django.core.paginator import Paginator, EmptyPage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.db import DatabaseError

class ApiView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    'Общий класс для составления ответа'

    def prepare_req_params(self, params):
        'Преобразуем гет параметры к словарю'
        dict_result = {}
        for (key, value) in params.items():
            if '[' in key and ']' in key:
                new_key = key[0:key.index('[')]

                if new_key not in dict_result:
                    dict_result[new_key] = {}

                sub_key = key[key.index('[')+1:-1]
                dict_result[new_key][sub_key] = value
            else:
                dict_result[key] = json.loads(value)

        return dict_result

    def parse_get_data(self, data):
        'Преобразуем ответ'
        res = {'fields': [], 'rows': []}

        for item in data:
            if not res['fields']:
                for key in item:
                    res['fields'].append(key)
            res['rows'].append(item.values())

        return res

    def _make_sort(self, req_params, sort, parent=None):
        qs_data = self.get_queryset()

        fltr = req_params.get('fltr', {})
        if fltr:
            qs_data = self.fltr(qs_data, fltr)

        sorting = req_params.get('sorting', {})

        if len(req_params['sorting']):
            sort = [('-' if sorting['sortDesc'] else '') + sorting['sortBy']]

        if 'parent' in [x.name for x in self.model._meta.fields]:
            qs_data = qs_data.filter(parent=parent)

        return qs_data.order_by(*sort)

    def _get_start_page_by_id(self, qs_data, one_row, sort, per_page):
        'по записи получаем страницу, откудпа будет старт'
        cnt = 0
        tmp_qs = qs_data.all()

        for item in sort:
            sign = 'lt'

            if item.startswith('-'):
                item = item[1:]
                sign = 'gt'

            value = one_row[item]
            if value is not None:
                condition = {item + '__' + sign: value}
            else:
                condition = {item + '__isnull': True}

            cnt += tmp_qs.filter(**condition).count()
            tmp_qs = tmp_qs.exclude(**condition)

        cnt += 1
        return [math.ceil(cnt / per_page), qs_data]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()

        req_params = self.prepare_req_params(request.query_params)

        # папка и выбранный по умолчанию элемент
        start_id = req_params.get('startId', None)
        parent = req_params.get('parent', None)

        if start_id:
            item =  serializer([self.objects.get(pk=start_id)], many=True).data[0]
            parent = item.get('parent', None)

        sort = getattr(self, 'default_sorting', ['id'])

        qs_data = None # QuerySet

        if 'pk' in kwargs:
            qs_data = [self.objects.get(pk=kwargs['pk'])]
        else:
            # сортировка
            qs_data = self._make_sort(req_params, sort, parent)

        pagination = req_params.get('pagination') or {
            'perPage': 10,
            'page': 0
        }
        per_page = int(pagination.get('perPage')) or 10
        page = int(pagination and pagination.get('page')) or 1

        if start_id:
            [page, qs_data] = self._get_start_page_by_id(
                qs_data,
                serializer([self.objects.get(pk=start_id)], many=True).data[0],
                sort, per_page
            )

        paginator = Paginator(qs_data, per_page)
        try:
            data_page = paginator.page(page)
        except EmptyPage:
            page = 1
            data_page = paginator.page(page)

        serialized_data = serializer(data_page, many=True)

        return Response(
            self.parse_get_data(serialized_data.data) | {
                'service': {
                    'count_rows': paginator.count,
                    'count_pages': paginator.num_pages,
                    'page': page,
                    'parent': parent
                }
            }
        )

    def patch(self, request, *args, **kwargs):
        try:
            return generics.RetrieveUpdateDestroyAPIView.patch(self, request, *args, **kwargs)
        except DatabaseError as error:
            return JsonResponse({
                'error': {
                    'message': error.args[0]
                }
            }, status=500)

    def move(self, data):
        'Перемещение элемента в выборке между папками'
        parent = data['pk'] if data['pk'] else None
        return self.objects.filter(pk__in=data['items']).update(parent=parent)

    def post(self, request, *args, **kwargs):
        'Содаем элементы, и работаем со своими методами'
        method = request.data.get('_method') and request.data['_method'].lower()
        if request.data.get('_method') and hasattr(self, method):
            if 'pk' in kwargs:
                request.data['pk'] = kwargs['pk']

            if request.data.get('bgTask'):
            # задача фоновая
                for key in request.data:
                    value = request.data[key]

                    if isinstance(value, InMemoryUploadedFile):
                        request.data[key] = base64.b64encode(value.read())

                res = getattr(self, method).delay(request.data)

                headers = {
                    'job-id': res.id,
                    'Access-Control-Expose-Headers': 'job-id'
                }

                return JsonResponse(data={}, status=202, headers=headers)

            res = getattr(self, method)(request.data)
            return JsonResponse({'data': res})

        try:
            return generics.CreateAPIView.post(self, request, *args, **kwargs)
        except DatabaseError as error:
            return JsonResponse({
            'error': {
                'message': error.args[0]
            }
            }, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            list_to_delete = json.loads(request.query_params.get('id', '[]'))
            if list_to_delete:
                if self.objects.filter(id__in=list_to_delete).delete()[0]:
                    return JsonResponse(data={})

            return generics.RetrieveUpdateDestroyAPIView.delete(self, request, *args, **kwargs)
        except DatabaseError as error:
            return JsonResponse({
                'error': {
                    'message': error.args[0]
                }
            }, status=500)
