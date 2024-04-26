from django.shortcuts import render
from .models import reports
from inventory.models import Equipment

# REPORT WEBSITE VIEW
def reportItems(request):
    items = reports.objects.all()
    return render(request, "report/report.html", {"items": items})
