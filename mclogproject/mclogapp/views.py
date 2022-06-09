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
from .serializers import CheckImoSerializer



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
            try:
                self.save_log_file(file)
                return HttpResponse("File uploaded successfully!")
            except:
                return HttpResponse ("File format is not valid!")
            # return HttpResponseRedirect( 'mclogapp/report.html')
        else:
            return HttpResponse("Upload can not be empty!")
            # return HttpResponseRedirect('mclogapp/report.html')

    def get(self, request):
        form=UploadLogFile
        return render(request, 'mclogapp/home.html', {'form':form})
    
    
    def save_log_file(self, file):
        file_data=file.read().decode("utf-8")
        lines=file_data.split("\n")
        lines.remove("")
        del lines[0]
        get_ship_object=ShipDetails.objects.get(shipImo=9838840)
        
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

    def __init__(self, create_cursor):
        self.create_cursor=create_cursor
        pass

    # def get(self, imo):
        """
        find ship with give IMO from all IMO tables, 
        then make direct query to group by date.
        Return date by month.
        """
        # pass

    @api_view(('GET',))
    def ship_names(self):
        ship_found =ShipDetails.objects.all()
        serializer=CheckImoSerializer(ship_found, many=True)
        print('--------',serializer)
        return Response(serializer.data)



        
    def create_cursor(query):
        with connection.cursor() as curs:
            curs.execute(query)
            columns=[col[0] for col in curs.description]
            result=[ zip(columns,  row)  for row in curs.fetchall()]
        return (result)

    @api_view(('GET',))
    def system_downtime(self):
        query=("""select TIMESTAMPDIFF(hour,  
                str_to_date( substring(logDescription, 36,19 ),"%d.%m.%Y %H:%i:%s" ), logDateTime ) as "System was down in hour" ,
                logDateTime as "System start" , 
                str_to_date(substring(logDescription, 36,19 ), "%d.%m.%Y %H:%i:%s" ) as "System shutdown"
                from  mclog_db.mclogapp_shiplogs  
                where logCategory = 'Info' and logDescription like'PLC Powered ON%' and  TIMESTAMPDIFF(hour,  
                str_to_date( substring(logDescription, 36,19 ),"%d.%m.%Y %H:%i:%s" ), logDateTime ) >1; """)
        
        result=SearchShipDetails.create_cursor(query)
        return Response (result)


    @api_view(('GET',))
    def operating_to_extend_open_position(self):
        query=("""
            with opp AS 
            (
            select *, substr( logDescription ,1,4) as "hcid"
            from mclog_db.mclogapp_shiplogs   
            where logCategory = 'Info'  and logDescription like '%Stopped automatic mode open position' 
            ) 
            , exp as (
            select *, substr( logDescription ,1,4) as "hcid"
            from mclog_db.mclogapp_shiplogs   
            where logCategory = 'Info'  and logDescription like  '%ext open position' 
            )

            select (
            select count(*) from opp, exp where opp.hcid = exp.hcid and TIMESTAMPDIFF( minute, opp.logDateTime, exp.logDateTime) between 0 and 15 
            ) as "Nummber of driving directly within 15mins", 
            (
            select count(*) from opp, exp where opp.hcid = exp.hcid and TIMESTAMPDIFF( minute, opp.logDateTime, exp.logDateTime) >16 
            ) as "Number of leaving panel in open position longer than 15mins"
            ;
        """)
        result=SearchShipDetails.create_cursor(query)
        return Response(result)

    @api_view(('GET',))
    def calibration_mismatch(self):
        query=("""
        select  *, clstarted.`Calibration started` - cldone.`Calibration done`   as "Incomplete calibration" from 
            (
            select substr(logDescription, 1,4) as HatchcoverID, count(logDescription) as "Calibration started" 
            from mclog_db.mclogapp_shiplogs 
            where logCategory="Info" and logDescription like "%calibration started%" group by logDescription
            )  as clstarted
            join 
            (
            select substr(logDescription, 1,4) as HatchcoverID, count(logDescription) as "Calibration done" 
            from mclog_db.mclogapp_shiplogs 
            where logCategory="Info" and logDescription like "%calibration done%" group by logDescription
            ) as cldone
            on clstarted.HatchcoverID = cldone.HatchcoverID
            order by 1;
        """)
        result=SearchShipDetails.create_cursor(query)
        return Response (result)

    @api_view(('GET',))
    def motor_stall_fault_manual_mode(self):
        query=("""
        select info.closingDate  as "Fault date"
            from(
            select *, date(logDateTime) as closingDate 
            from mclog_db.mclogapp_shiplogs 
            where logCategory = "Info" and logDescription like "%Closing manual mode%" order by id
            ) as info join (
            select *, date(logDateTime) as stallDate  
            from mclog_db.mclogapp_shiplogs 
            where logCategory = "Fault" and logDescription like "%Motor stall%" order by id
            ) as fault
            on info.closingDate = fault.stallDate
            group by info.closingDate order by 1;
        """)
        result = SearchShipDetails.create_cursor(query)
        return Response(result)

    def pushing_against_panels(self):
        pass

    def motor_heating_duration(self):
        pass