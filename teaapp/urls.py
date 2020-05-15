from django.urls import path
from teaapp import views
from .views import *

app_name = "teaapp"

urlpatterns = [
    path('', tea_list, name='tea_list'),
    path('teas/add', tea_form, name='tea_form')
]
