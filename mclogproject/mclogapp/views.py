
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render


from rest_framework.views import APIView
from .forms import UploadLogFile
from .models import ShipDetails

import csv


#----------------------------------------------------------
def index(request):
    return HttpResponse('from View')


#----------------------------------------------------------
class LogFileProcess(APIView):
    def __init__(self) -> None:
        pass
    
    def post(self, request):
        if (request.FILES):
            # get_file_name=list(request.FILES.keys())
            # Only one file is supposed to be uploaded, so [0] will do the job
            # 
            # self.show_file_content(request.FILES[get_file_name[0]])
            csv_file=request.FILES["csv_file"]
            file_data=csv_file.read().decode("utf-8")
            lines=file_data.split("\n")
            for line in lines:
                # fields=line.split(';')
                print(line)
                # print(fields[1])
                # print(fields[2])
            return HttpResponse("file received")
            # return HttpResponseRedirect( 'mclogapp/report.html')
        else:
            return HttpResponse("file is not valid")
            # return HttpResponseRedirect('mclogapp/report.html')

    

    def get(self, request):
        form=UploadLogFile
        return render(request, 'mclogapp/home.html', {'form':form})

    def read_file(self,file):
        imo = imo
        self.search_ship(imo, file)
        pass
    
    def insert_to_db(records):
        pass

    def create_db(shipinfo):
        pass
    
    def search_ship(self, imo, file):
        
        try:
            shipFound = ShipDetails.objects.get(shipImo = imo)
            self.insert_to_db(file)

        except ObjectDoesNotExist:
            self.create_db(imo)
        

    def show_file_content(self, file):
        # pd.read_csv(link, skiprows=2)
        file_content=list(file)
        for row in file_content:
            print (row)
        # for chunk in file.chunks():
            # print('--------',chunk)

#----------------------------------------------------------
class TransferringFile():
     # write dynamic sql here
    def import_file_to_db():
        pass


#----------------------------------------------------------
# presentation structure 