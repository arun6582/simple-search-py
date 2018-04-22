from . import apis
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from database import apis as db_apis
from django.views.generic import View
import json


def home(request):
    return render(request, 'index.html', {})


def index(request):
    data = request.POST['data']
    id = request.POST['id']
    title = request.POST['title']
    apis.Index.index({
        'id': id,
        'title': title,
        'data': data
    })
    return JsonResponse({'acknowledged': True})


def search(request):
    fields = request.GET.getlist('fields')
    query = request.GET['query']

    response = apis.Index.search(
        {
            'fields': fields or ['_all', ],
            'terms': query
        }
    )
    return JsonResponse({'data': response})


@method_decorator(csrf_exempt, name='dispatch')
class Meta(View):

    def get(self, request, *args, **kwargs):
        try:
            return JsonResponse(
                {
                    'success': True,
                    'document': db_apis.Operation.retrieve(
                        request.GET['document']
                    )
                }
            )
        except IOError:
            return JsonResponse({'success': False})

    def post(self, request, *args, **kwargs):
        js = json.loads(request.body)
        document = js['document']
        data = js['data']
        try:
            return JsonResponse(
                {
                    'success': True,
                    'document': db_apis.Operation.save(document, data)
                }
            )
        except IOError:
            return JsonResponse({'success': False})
