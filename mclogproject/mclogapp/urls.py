from urllib import request
from django.urls import  path
from . import views
from .views import LogFileProcess, SearchShipDetails

urlpatterns=[
    path('',views.index, name="index" ),
    path('home',  LogFileProcess.as_view() , name="home"),
    path('search', SearchShipDetails.system_downtime, name="search"),
]