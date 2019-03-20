import django_tables2 as tables
from .models import Nxos_vlan_svi


class vlan_table(tables.Table):
    class Meta:
        model = Nxos_vlan_svi
        template_name = 'django_tables2/semantic.html'
