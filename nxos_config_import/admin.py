from django.contrib import admin

from .models import Nxos_vlan_svi, FvAEPg, EpgInputForm

admin.site.register(Nxos_vlan_svi)
admin.site.register(FvAEPg)
admin.site.register(EpgInputForm)