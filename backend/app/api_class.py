from rest_framework.response import Response
from rest_framework import generics
from django.core.paginator import Paginator
from django.http import HttpResponse

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
        newKey = key
        dict[newKey] = value
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
    req_params = self.prepare_req_params(request.query_params)
    qs = None
    if 'pk' in kwargs:
      qs = [self.objects.get(pk=kwargs['pk'])]
    else:
      qs = self.get_queryset().order_by('id')

    serializer = self.get_serializer_class()

    try:
      per_page = int(req_params['pagination']['perPage'])
      page = int(req_params['pagination']['page'])
    except:
      per_page = 25
      page = 1

    paginator = Paginator(qs, per_page)
    try:
      data_page = paginator.page(page)
    except:
      data_page = paginator.page(1)
    
    dt = serializer(data_page, many=True)
    data = self.parse_get_data(dt.data)
    data['pagination'] = {}
    data['pagination']['count_rows'] = paginator.count
    data['pagination']['count_pages'] = paginator.num_pages
    return Response(data)
  
  def patch(self, request, *args, **kwargs):
    return generics.RetrieveUpdateDestroyAPIView.patch(self, request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    # доп метод перехватываем
    if bool(request.data.get('_method')):
      if 'pk' in kwargs:
        request.data['pk'] = kwargs['pk']
      method = request.data.get('_method').lower()
      if hasattr(self, method):
        res = getattr(self, method)(request.data)
        return res
  
    return generics.CreateAPIView.post(self, request, *args, **kwargs)
  
  def delete(self, request, *args, **kwargs):
    try:
      generics.RetrieveUpdateDestroyAPIView.delete(self, request, *args, **kwargs)
      return HttpResponse("ОК")
    except:
      return HttpResponse("False")
