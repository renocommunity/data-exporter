from django.shortcuts import render

from .models import RecordHandler

from django.http import HttpResponse, HttpResponseNotFound


def index(request):
    return HttpResponse("Hello, world!")

def get_data_as_json_file(request, record_handler_name):
    try:
        record_handler = RecordHandler.objects.get(name=record_handler_name)
    except RecordHandler.DoesNotExist:
        return HttpResponseNotFound(f"Record handler \"{record_handler_name}\" does not exist")
    json = record_handler.get_records_as_json()
    return HttpResponse(json, content_type='application/json')