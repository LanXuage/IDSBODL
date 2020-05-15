from django.shortcuts import render
from .models import NidsDatas, NidsProtocolTypes, NidsServices, NidsFlags, NidsLabels, Users
from .idsbodl import Idsbodl
from django.db.models import Count

# Create your views here.

def index(req):
    content = {
        'NidsDatas_count': NidsDatas.objects.count(),
        'NidsLabels_count': NidsLabels.objects.count(),
        'NidsServices_count': NidsServices.objects.count(),
        'Users_count': Users.objects.count(),
        'Collector_count': len(Idsbodl.get_collectors()),
    }
    return render(req, 'web/index.html', content)

def nidsdatas(req):
    page = req.GET.get('p')
    if page:
        page = int(page)
    else:
        page = 1
    content = {
        'NidsDatas': NidsDatas.objects.all()[10 * (page - 1) : 10 * page],
    }
    return render(req, 'web/nidsdatas.html', content)

