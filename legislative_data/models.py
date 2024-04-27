from django.db import models


class Person(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.id)
    

class Bill(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=50)
    sponsor_id = models.ForeignKey(Person, on_delete=models.CASCADE)
   
    def __str__(self) -> str:
        return str(self.id)
    

class Vote(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
   
    def __str__(self) -> str:
        return str(self.id)
    

class VoteResult(models.Model):
    id = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    legislator_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    vote_id = models.ForeignKey(Vote, on_delete=models.CASCADE)
    vote_type = models.IntegerField()
   
    def __str__(self) -> str:
        return str(self.id)