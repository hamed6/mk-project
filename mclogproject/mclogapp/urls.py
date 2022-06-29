# from urllib import request
from django.urls import  path
from . import views
from .views import LogFileProcess, SearchShipDetails

urlpatterns=[
    path('home',  LogFileProcess.as_view() , name="home"),
    path('', SearchShipDetails.as_view(), name="search"),
    path('<int:imo>/downtime', SearchShipDetails.system_downtime, name="system downtime"),
    path('<int:imo>/extendopen', SearchShipDetails.operating_to_extend_open_position, name="exten open position"),
    path('<int:imo>/calibration', SearchShipDetails.calibration_mismatch, name="calibration difference"),
    path('<int:imo>/stall', SearchShipDetails.motor_stall_fault_manual_mode, name="stall fault"),
    # path('dt', SearchShipDetails.system_donwtime_django, name="stall fault"),
]