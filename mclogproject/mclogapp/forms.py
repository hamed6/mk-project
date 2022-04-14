import csv
from django import forms


class UploadLogFile(forms.Form):
    ship_imo = forms.IntegerField( )
    ship_name = forms.CharField(max_length=25)
    ship_log_file = forms.FileField()
