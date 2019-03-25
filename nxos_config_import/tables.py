import django_tables2 as tables
from .models import Nxos_vlan_svi, FvAEPg, EpgInputForm, ObjectConfigurationStatus, FvBD


class vlan_table(tables.Table):
    class Meta:
        model = Nxos_vlan_svi
        template_name = 'django_tables2/semantic.html'


class epg_table(tables.Table):
    class Meta:
        model = FvAEPg
        template_name = 'django_tables2/semantic.html'


class BdTable(tables.Table):
    class Meta:
        model = FvBD
        template_name = 'django_tables2/semantic.html'


class epg_form_table(tables.Table):
    class Meta:
        model = EpgInputForm
        template_name = 'django_tables2/semantic.html'


class ObjectConfigurationTable(tables.Table):
    class Meta:
        model = ObjectConfigurationStatus
        template_name = 'django_tables2/semantic.html'

