from rest_framework.response import Response
from rest_framework import generics
from django.core.paginator import Paginator
from django.http import HttpResponse
import json
import math

class ApiView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
  def prepare_req_params(self, params):
    dict = {}
    for (key, value) in params.items():
      if '[' in key and ']' in key:
        newKey = key[0:key.index('[')]
        if newKey not in dict:
          dict[newKey] = {}
        sub_key = key[key.index('[')+1:-1]
        dict[newKey][sub_key] = value
      else:
        dict[key] = json.loads(value)

    return dict

  def parse_get_data(self, data):
    res = {'fields': [], 'rows': []}

    for item in data:
      if not len(res['fields']):
        for key in item:
          res['fields'].append(key)
      res['rows'].append(item.values())
    
    return res

  def get(self, request, *args, **kwargs):
    serializer = self.get_serializer_class()

    req_params = self.prepare_req_params(request.query_params)
    qs = None # QuerySet

    if 'pk' in kwargs:
      qs = [self.objects.get(pk=kwargs['pk'])]
    else:
      # сортировка
      sort = getattr(self, 'default_sorting', ['id'])
      sorting = req_params.get('sorting', {})
      if len(req_params['sorting']):
        sort = [('-' if sorting['sortDesc'] else '') + sorting['sortBy']]

      # папка и выбранный по умолчанию элемент
      parent = req_params.get('parent', None)
      start_id = req_params.get('startId', None)
      
      qs = self.get_queryset()

      if 'parent' in [x.name for x in self.model._meta.fields] and not start_id:
        qs = qs.filter(parent=parent)

      qs = qs.order_by(*sort)

    try:
      per_page = int(req_params['pagination']['perPage'])
      page = int(req_params['pagination']['page'])
      if start_id:
        row = [self.objects.get(pk=start_id)]
        dt = (serializer(row, many=True).data)[0]
        parent = dt.get('parent', None)
        if parent:
          qs = qs.filter(parent=parent)
        
        cnt = 0
        tmp_qs = qs.all()
        for item in sort:
          lt = {}
          sign = 'lt'
          if item.startswith('-'):
            item = item[1:]
            sign = 'gt'
          lt[item + '__' + sign] = dt[item]

          cnt += tmp_qs.filter(**lt).count()
          tmp_qs = tmp_qs.exclude(**lt)

        cnt += 1
        page = math.ceil(cnt / per_page)
    except:
      per_page = 10
      page = 1

    paginator = Paginator(qs, per_page)
    try:
      data_page = paginator.page(page)
    except:
      page = 1
      data_page = paginator.page(page)
    
    dt = serializer(data_page, many=True)
    data = self.parse_get_data(dt.data)
  
    data['service'] = {}
    data['service']['count_rows'] = paginator.count
    data['service']['count_pages'] = paginator.num_pages
    data['service']['page'] = page
    data['service']['parent'] = locals().get('parent')

    return Response(data)
  
  def patch(self, request, *args, **kwargs):
    return generics.RetrieveUpdateDestroyAPIView.patch(self, request, *args, **kwargs)

  def move(self, data):
    parent = data['pk'] if data['pk'] else None
    return self.objects.filter(pk__in=data['items']).update(parent=parent)

  def post(self, request, *args, **kwargs):
    # доп метод перехватываем
    if bool(request.data.get('_method')):
      if 'pk' in kwargs:
        request.data['pk'] = kwargs['pk']
      method = request.data.get('_method').lower()
      if hasattr(self, method):
        try:
          res = getattr(self, method)(request.data)
          return HttpResponse(json.dumps({'data': res}))
        except Exception as e:
          pgcode = getattr(e.__cause__, 'pgcode', False) if getattr(e, '__cause__', False) else None
          message = str(e)
          return HttpResponse(json.dumps({
            'error': {
              'pgcode': pgcode,
              'message': message
            }
          }, ensure_ascii=False), status=500)
  
    return generics.CreateAPIView.post(self, request, *args, **kwargs)
  
  def delete(self, request, *args, **kwargs):
    try:
      return generics.RetrieveUpdateDestroyAPIView.delete(self, request, *args, **kwargs)
    except Exception as e:
      return HttpResponse(json.dumps({
        'error': {
          'message': e.args[0]
        }
      }), status=500)
