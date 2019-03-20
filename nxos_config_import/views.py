from django.shortcuts import render
from django_tables2 import RequestConfig

from .models import Nxos_vlan_svi
from .tables import vlan_table




from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, world. You're at the nxos config import index.")


def vlans_data(request):
    table = vlan_table(Nxos_vlan_svi.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'nxos_config_import/vlans.html', {'table': table})

