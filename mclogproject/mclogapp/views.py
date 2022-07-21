import datetime as dt

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import Http404, HttpResponse
from django.shortcuts import render
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
class SearchShipDetails(APIView):
    
    def __init__(self):
        pass
    
    def get(self, request):
        ships= ShipDetails.objects.all()
        ship_imo=[ship.shipImo for ship in ships]
        return Response(ship_imo)

    

    @api_view(('GET',))
    def ship_names(self):
        # ships =[ship.shipName, ship.shipImo for ship in ShipDetails.objects.all()]
        ships= ShipDetails.objects.all()
        serializer=CheckImoSerializer(ships, many=True)
        return Response(serializer.data)
        
    def create_cursor_one_imo( query, imo=""):
        with connection.cursor() as curs:
            if imo != "":
                curs.execute(query, [imo])
            else:
                curs.execute(query)
            columns=[col[0] for col in curs.description]
            result=[ zip(columns,  row)  for row in curs.fetchall()]
        return (result)

    def create_cursor_two_imo( query, first_id="", second_id=""):
        with connection.cursor() as curs:
            curs.execute(query, [first_id,second_id])
            columns=[col[0] for col in curs.description]
            result=[ zip(columns,  row)  for row in curs.fetchall()]
        return (result)
    
    
    def find_ship_imo(id):
        try:
            get_ship=ShipDetails.objects.get(shipImo=id)
            return (get_ship)
        except ShipDetails.DoesNotExist:
            raise Http404


    @api_view(('GET',))
    def system_downtime( self, imo):
        # get_imo_id=ShipDetails.objects.get(shipImo=imo)
        # ship_id=SearchShipDetails.find_ship_imo(imo)
        ship_id=SearchShipDetails.find_ship_imo(imo)
        query=('''select TIMESTAMPDIFF(hour,  
                str_to_date( substring(logDescription, 36,19 ), "%%d.%%m.%%Y %%H:%%i:%%s" ), logDateTime ) as "System was down in hour" ,
                logDateTime as "System start" , 
                str_to_date(substring(logDescription, 36,19 ), "%%d.%%m.%%Y %%H:%%i:%%s" ) as "System shutdown"
                from  mclog_db.mclogapp_shiplogs  
                where  logImo_id =%s and  logCategory = 'Info' and logDescription like'PLC Powered ON%%' and  TIMESTAMPDIFF(hour,  
                str_to_date( substring(logDescription, 36,19 ),"%%d.%%m.%%Y %%H:%%i:%%s" ), logDateTime ) >1; ''')
        
        result=SearchShipDetails.create_cursor_one_imo(query, ship_id.id)
        return Response (result)


    @api_view(('GET',))
    def operating_to_extend_open_position(self, imo):
        ship_id=SearchShipDetails.find_ship_imo(imo)
        query=("""
            with opp AS 
            (
            select *, substr( logDescription ,1,4) as "hcid"
            from mclog_db.mclogapp_shiplogs   
            where logImo_id =%s and logCategory = 'Info'  and logDescription like '%%Stopped automatic mode open position' 
            ) 
            , exp as (
            select *, substr( logDescription ,1,4) as "hcid"
            from mclog_db.mclogapp_shiplogs   
            where logImo_id =%s and  logCategory = 'Info'  and logDescription like  '%%ext open position' 
            )

            select (
            select count(*) from opp, exp where opp.hcid = exp.hcid and TIMESTAMPDIFF( minute, opp.logDateTime, exp.logDateTime) between 0 and 15 
            ) as "Nummber of driving directly within 15mins", 
            (
            select count(*) from opp, exp where opp.hcid = exp.hcid and TIMESTAMPDIFF( minute, opp.logDateTime, exp.logDateTime) >16 
            ) as "Number of leaving panel in open position longer than 15mins"
            ;
        """)
        result=SearchShipDetails.create_cursor_two_imo(query, ship_id.id ,ship_id.id)
        return Response(result)

    @api_view(('GET',))
    def calibration_mismatch(self, imo):
        ship_id=SearchShipDetails.find_ship_imo(imo)
        query=("""
        select  *, clstarted.`Calibration started` - cldone.`Calibration done`   as "Incomplete calibration" from 
            (
            select substr(logDescription, 1,4) as HatchcoverID, count(logDescription) as "Calibration started" 
            from mclog_db.mclogapp_shiplogs 
            where logImo_id =%s and logCategory="Info" and logDescription like "%%calibration started%%" group by logDescription
            )  as clstarted
            join 
            (
            select substr(logDescription, 1,4) as HatchcoverID, count(logDescription) as "Calibration done" 
            from mclog_db.mclogapp_shiplogs 
            where logImo_id =%s and logCategory="Info" and logDescription like "%%calibration done%%" group by logDescription
            ) as cldone
            on clstarted.HatchcoverID = cldone.HatchcoverID
            order by 1;
        """)
        result=SearchShipDetails.create_cursor_two_imo(query, ship_id.id ,ship_id.id)
        return Response (result)

    @api_view(('GET',))
    def motor_stall_fault_manual_mode(self, imo):
        ship_id=SearchShipDetails.find_ship_imo(imo)
        query=("""
        select info.closingDate  as "Fault date"
            from(
            select *, date(logDateTime) as closingDate 
            from mclog_db.mclogapp_shiplogs 
            where logImo_id =%s and logCategory = "Info" and logDescription like "%%Closing manual mode%%" order by id
            ) as info join (
            select *, date(logDateTime) as stallDate  
            from mclog_db.mclogapp_shiplogs 
            where logImo_id =%s and logCategory = "Fault" and logDescription like "%%Motor stall%%" order by id
            ) as fault
            on info.closingDate = fault.stallDate
            group by info.closingDate order by 1;
        """)
        result=SearchShipDetails.create_cursor_two_imo(query, ship_id.id ,ship_id.id)
        return Response(result)

    def pushing_against_panels(self):
        pass

    def motor_heating_duration(self):
        pass
    
    # @api_view(('GET',))
    # def system_donwtime_django(self):
    #     imo="2"
    #     query=(" select count(*) from mclog_db.mclogapp_shiplogs where logImo_id=%s;")
    #     result =SearchShipDetails.create_cursor_one_imo(query, imo)
    #     return Response(result)
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
        
