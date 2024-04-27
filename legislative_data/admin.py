import csv
import io

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from .models import Bill, Person, Vote, VoteResult

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField(label="CSV File")

class CsvUploadAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path("upload-csv/", self.upload_csv),]
        return new_urls + urls
    
    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(request, "The wrong type was uploaded")
                return HttpResponseRedirect(request.path_info)
           
            file_data = list(csv.reader(io.TextIOWrapper(csv_file.open()), delimiter=","))

            for data in file_data[1:]:
                try:
                    self.process_csv(data)
                except Exception as err:
                    messages.warning(request, err)
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)
    
    def process_csv(self, file_data):
        raise NotImplementedError()

class PersonAdmin(CsvUploadAdmin):
    list_display = ("id", "name")
    
    def process_csv(self, file_data):
            id, name = file_data
            Person.objects.update_or_create(id=id, name=name)

class BillAdmin(CsvUploadAdmin):
    list_display = ("id", "title", "sponsor_id")
    
    def process_csv(self, file_data):
        id, title, sponsor_id = file_data
        try:
            primary_sponsor = Person.objects.get(id=sponsor_id)
            Bill.objects.update_or_create(id=id, title=title, sponsor_id=primary_sponsor)
        except:
            raise ValueError(
                f"Couldn't find Legislator with id: '{sponsor_id}'"
            )
        

class VoteAdmin(CsvUploadAdmin):
    list_display = ("id", "bill_id")
    
    def process_csv(self, file_data):
        id, bill_id = file_data
        try:
            bill = Bill.objects.get(id=bill_id)
            Vote.objects.update_or_create(id=id, bill_id=bill)
        except:
            raise ValueError(
                f"Couldn't find Bill with id: '{bill_id}'"
            )
        

class VoteResultAdmin(CsvUploadAdmin):
    list_display = ("id", "legislator_id", "vote_id", "vote_type")
    
    def process_csv(self, file_data):
        id, legislator_id, vote_id, vote_type = file_data
        try:
            legislator = Person.objects.get(id=legislator_id)
            vote = Vote.objects.get(id=vote_id)
            VoteResult.objects.update_or_create(id=id, legislator_id=legislator, vote_id=vote, vote_type=vote_type)
        except:
            raise ValueError(
                f"Couldn't find Vote Result"
            )

admin.site.register(Person, PersonAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(VoteResult, VoteResultAdmin)
