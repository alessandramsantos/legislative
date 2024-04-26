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
                self.process_csv(data)
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


admin.site.register(Person, PersonAdmin)
# admin.site.register(Bill, BillsAdmin)
# admin.site.register(Vote, VoteAdmin)
# admin.site.register(VoteResult, VoteResultAdmin)
