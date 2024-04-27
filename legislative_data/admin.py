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

class BaseAdmin(admin.ModelAdmin):

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
    

class PersonAdmin(BaseAdmin):
    list_display = ["id", "name"]
    fields = ["id", "name", "supported_bills", "opposed_bills"]
    readonly_fields = ["supported_bills", "opposed_bills"]
    
    def process_csv(self, file_data):
            id, name = file_data
            Person.objects.update_or_create(id=id, name=name)

    def supported_bills(self, obj):
        supported_bills = VoteResult.objects.filter(legislator_id=obj.id, vote_type=1).count()
        return supported_bills
    
    supported_bills.short_description = "Supported Bills"
    
    def opposed_bills(self, obj):
        opposed_bills = VoteResult.objects.filter(legislator_id=obj.id, vote_type=2).count()
        return opposed_bills
    
    opposed_bills.short_description = "Opposed Bills"

class BillAdmin(BaseAdmin):
    list_display = ["id", "title", "sponsor_id"]
    fields = ["id", "title", "primary_sponsor", "supported_legislators", "opposed_legislators"]
    readonly_fields = ["supported_legislators", "opposed_legislators", "primary_sponsor"]
    
    def process_csv(self, file_data):
        id, title, sponsor_id = file_data
        try:
            primary_sponsor = Person.objects.get(id=sponsor_id)
            Bill.objects.update_or_create(id=id, title=title, sponsor_id=primary_sponsor)
        except:
            raise ValueError(
                f"Couldn't find Legislator with id: '{sponsor_id}'"
            )

    def supported_legislators(self, obj):
        supported_legislators = VoteResult.objects.filter(vote_id__bill_id=obj.id, vote_type=1).count()
        return supported_legislators
    
    supported_legislators.short_description = "Supported Legislators"

    def opposed_legislators(self, obj):
        opposed_legislators = VoteResult.objects.filter(vote_id__bill_id=obj.id, vote_type=2).count()
        return opposed_legislators
    
    opposed_legislators.short_description = "Opposed Legislators"

    def primary_sponsor(self, obj):
        return obj.sponsor_id.name
    
    primary_sponsor.short_description = "Primary Sponsor"

class VoteAdmin(BaseAdmin):
    list_display = ["id", "bill_id"]
    
    def process_csv(self, file_data):
        id, bill_id = file_data
        try:
            bill = Bill.objects.get(id=bill_id)
            Vote.objects.update_or_create(id=id, bill_id=bill)
        except:
            raise ValueError(
                f"Couldn't find Bill with id: '{bill_id}'"
            )
        

class VoteResultAdmin(BaseAdmin):
    list_display = ["id", "legislator_id", "vote_id", "vote_type"]
    
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