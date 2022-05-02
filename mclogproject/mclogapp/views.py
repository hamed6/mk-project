import datetime as dt

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db import connection

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import UploadLogFile
from .models import ShipDetails, ShipLogs




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
            """
             Only one file is supposed to be uploaded, so [0] will do the job
            """
            # self.save_log_file(request.FILES[get_file_name[0]])
            file=request.FILES["csv_file"]
            self.save_log_file(file)

            return HttpResponse("file received")
            # return HttpResponseRedirect( 'mclogapp/report.html')
        else:
            return HttpResponse("file is not valid")
            # return HttpResponseRedirect('mclogapp/report.html')

    def get(self, request):
        form=UploadLogFile
        return render(request, 'mclogapp/home.html', {'form':form})
    
    
    def save_log_file(self, file):
            file_data=file.read().decode("utf-8")
            lines=file_data.split("\n")
            lines.remove("")
            del lines[0]
            get_ship_object=ShipDetails.objects.get(shipImo=2)
            
            for line in lines: 
                field=line.split(';')
                # field=line.strip()
                # dd=field[0].split(' ')
                # correct_date=dt.datetime.strptime(dd[0],'%d.%m.%Y')
                # correct_time=dt.datetime.strptime(dd[1], '%H:%M:%S')
                translate_date=dt.datetime.strptime(field[0],'%d.%m.%Y %H:%M:%S' )
                format_date=dt.datetime.strftime(translate_date, '%Y-%m-%d %H:%M:%S')
                
                shiplogtable=ShipLogs(
                logImo=get_ship_object
                , logDateTime=format_date
                , logCategory=field[1]
                , logDescription=field[2]
                # , logDate=correct_date
                # , logTime=correct_time
                # , logExtranote=field[3]
                )
                shiplogtable.save()
            # pd.read_csv(link, skiprows=2)
            # file_content=list(file)
            # for row in file_content:
                # print (row)
            # for chunk in file.chunks():
                # print('--------',chunk)

    def read_file(self,file):
        pass
    

    def create_db(shipinfo):
        """
        from django.db import connection

        # Create a connection with your database
        cursor = connection.cursor()

        # Execute your raw SQL
        cursor.execute("CREATE TABLE NameTable(name varchar(255));")
        # Create database records
        cursor.execute("INSERT INTO NameTable VALUES('ExampleName')")
        # Fetch records from the database
        cursor.execute("SELECT * FROM NameTable")

        # Get the data from the database. fetchall() can be used if you would like to get multiple rows
        name = cursor.fetchone()

        # Manipulate data
        # Don't forget the close database connection
        cursor.close()
        """
        pass
    def search_ship(self, imo, file):
        try:
            ship_found = ShipDetails.objects.get(shipImo = imo)
            self.insert_to_db(file)

        except ObjectDoesNotExist:
            self.create_db(imo)
        


#----------------------------------------------------------
class SearchShipDetails(APIView):

    # def get_table_name(self):
    #     table_name='mclog_db.mclogapp_shipdetails'
    #     return table_name

    def __init__(self):
        pass

    def get(self, imo):
        """
        find ship with give IMO from all IMO tables, 
        then make direct query to group by date.
        Return date by month.
        """
        ship_log_object=ShipLogs.objects.get(logImo=imo)
        return (ship_log_object)
    
    @api_view(('GET',))
    def system_downtime(self):
        query=("""select TIMESTAMPDIFF(hour, logDateTime, 
                str_to_date( substring(logDescription, 36,19 ),
                "%d.%m.%Y %H:%i:%s" ) ), logDateTime, 
                str_to_date(substring(logDescription, 36,19 ), "%d.%m.%Y %H:%i:%s" )
                from  mclog_db.mclogapp_shiplogs  
                where logCategory = 'Info' and logDescription like'PLC Powered ON%' """)
        with connection.cursor() as c:
            c.execute(query)
            c=c.fetchall()
        return Response (c)


    def operating_to_extend_open_position(self):
        pass

    def calibration_mismatch(self):
        pass

    def motor_stalled_fault_manual_mode(self):
        pass

    def pushing_against_panels(self):
        pass

    def motor_heating_duration(self):
        pass