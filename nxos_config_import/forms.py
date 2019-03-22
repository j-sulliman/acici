from django import forms
from .models import FvAEPg, EpgInputForm, PushDataApic
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class EpgForm(forms.ModelForm):
    class Meta:
        model = EpgInputForm
        fields = ('apic_addr',
                  'default_tenant',
                  'default_ipg_name',
                  'physical_domain',
                  'migration_leafs_nodeid')

class PushDataForm(forms.ModelForm):
    class Meta:
        model = PushDataApic
        fields = ('apic_addr',
                  'password')



