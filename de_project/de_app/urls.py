from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:record_handler_name>/data-as-json-file', views.get_data_as_json_file)
]