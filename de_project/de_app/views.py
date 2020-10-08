from django.shortcuts import render

from .models import RecordHandler

from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    return HttpResponse("Hello, world!")

def get_data_as_json_file(request, record_handler_name):
    record_handler = RecordHandler.objects.get(name=record_handler_name)
    json = record_handler.get_records_as_json()
    return HttpResponse(json, content_type='application/json')