from django.db import models

class ShipDetails(models.Model):
    shipImo=models.IntegerField(blank=False, null=False)
    shipName=models.CharField(blank=False, null=False)
    
    def __str__(self):
        return self.shipName

    

class ShipLogs(models.Model):
    logImo=models.ForeignKey(ShipDetails, on_delete=models.CASCADE)
    logDate=models.DateField()
    logTime=models.TimeField()
    logCategory=models.CharField()
    logDescription=models.CharField()
    logExtranote=models.CharField(default='')
    

    def __str__(self):
        return self.logCategory