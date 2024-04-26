from django.db import models


class Legislator(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return self.name
    

class Bill(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=50)
    primary_sponsor = models.ForeignKey(Legislator, on_delete=models.CASCADE)
   
    def __str__(self) -> str:
        return self.title