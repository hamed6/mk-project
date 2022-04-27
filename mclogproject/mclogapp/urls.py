from django.urls import  path
from . import views
from .views import LogFileProcess, SearchShipDetails

urlpatterns=[
    path('',views.index, name="index" ),
    path('home',  LogFileProcess.as_view() , name="home"),
    path('search', SearchShipDetails.as_view(), name="search")
]