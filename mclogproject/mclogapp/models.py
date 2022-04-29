from django.db import models


class ShipDetails(models.Model):
    shipImo=models.IntegerField(unique=True, blank=False, null=False)
    shipName=models.CharField(max_length=25, blank=False, null=False)
    # shiplogFile=models.FileFielde()
    # last file uploaded date, name 
    # project number, hall number, any details about mck
    def __str__(self):
        return self.shipName

    

class ShipLogs(models.Model):
    logImo=models.ForeignKey(ShipDetails, on_delete=models.CASCADE)
    # logDate=models.DateField()
    # logTime=models.TimeField()
    logDateTime=models.DateTimeField(default='1970-01-01 00:00:10')
    logCategory=models.CharField(max_length=25)
    logDescription=models.CharField(max_length=100)
    # logExtranote=models.CharField(max_length=100)
    
    class Meta:
        ordering=['logDateTime']

    def __str__(self):
        return self.logCategory