from django.contrib import admin

from .models import Nxos_vlan_svi, FvAEPg, EpgInputForm, PushDataApic, Document


admin.site.site_header = "ACI Configuration Generator Admin Portal"
admin.site.site_title = "ACI Configuration Generator Admin Portal"
admin.site.index_title = "Welcome to ACI Configuration Generator Admin Portal"
admin.site.register(Nxos_vlan_svi)
admin.site.register(FvAEPg)
admin.site.register(EpgInputForm)
admin.site.register(PushDataApic)
admin.site.register(Document)