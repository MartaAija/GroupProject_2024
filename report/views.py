#   WORKED ON FILE:
#        - NOEL VARGA (w1932378)

from django.shortcuts import render
from .models import reports
from inventory.models import Equipment
from django.contrib.auth.decorators import login_required

# REPORT WEBSITE VIEW
@login_required
def reportItems(request):
    items = reports.objects.all()
    # CHECKS FOR CURRENT USER TYPE
    currentUser = request.user
    return render(request, "report/report.html", {"items": items, "currentUser" : currentUser})
