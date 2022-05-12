from urllib import request
from django.urls import  path
from . import views
from .views import LogFileProcess, SearchShipDetails

urlpatterns=[
    path('home',  LogFileProcess.as_view() , name="home"),
    path('', SearchShipDetails.ship_names, name="search"),
    path('downtime', SearchShipDetails.system_downtime, name="system downtime"),
    path('extendopen', SearchShipDetails.operating_to_extend_open_position, name="exten open position"),
    path('calibration', SearchShipDetails.calibration_mismatch, name="calibration difference"),
    path('stall', SearchShipDetails.motor_stall_fault_manual_mode, name="stall fault"),
]