
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render


from rest_framework.views import APIView
from .forms import UploadLogFile
from .models import ShipDetails



#----------------------------------------------------------
def index(request):
    return HttpResponse('from View')


#----------------------------------------------------------
class LogFileProcess(APIView):
    def __init__(self) -> None:
        pass
    
    def post(self, request):
        print(request)
        if (request.FILES):
            get_file_name=list(request.FILES.keys())
            # Only one file is supposed to be uploaded, so [0] will do the job
            self.show_file_content(request.FILES[get_file_name[0]])
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
        for chunk in file.chunks():
            print('--------',chunk)
#----------------------------------------------------------
class TransferringFile():
     # write dynamic sql here
    def import_file_to_db():
        pass


#----------------------------------------------------------
# presentation structure 