from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView

from .models import ShipDetails

def index(request):
    return HttpResponse('from View')



class LogFileProcess(APIView):
    def __init__(self) -> None:
        pass
    
    
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
        

    def show_file_content(self):
        # return json file content with proper format
        pass

class TransferringFile():
     # write dynamic sql here
    def import_file_to_db():
        pass



# presentation structure 