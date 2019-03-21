import django_tables2 as tables
from .models import Nxos_vlan_svi, FvAEPg, EpgInputForm


class vlan_table(tables.Table):
    class Meta:
        model = Nxos_vlan_svi
        template_name = 'django_tables2/semantic.html'


class epg_table(tables.Table):
    class Meta:
        model = FvAEPg
        template_name = 'django_tables2/semantic.html'


class epg_form_table(tables.Table):
    class Meta:
        model = EpgInputForm
        template_name = 'django_tables2/semantic.html'

