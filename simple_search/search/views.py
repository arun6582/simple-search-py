from . import apis
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, 'index.html', {})


def index(request):
    apis.Index.index(dict(request.POST))
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
