from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Nxos_vlan_svi, FvAEPg, EpgInputForm
from .tables import vlan_table, epg_table, epg_form_table
from .forms import EpgForm




from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Hello, world. You're at the nxos config import index.")


def vlans_data(request):
    table = vlan_table(Nxos_vlan_svi.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'nxos_config_import/vlans.html', {'table': table})


def epgs_data(request):
    epgtable = epg_table(FvAEPg.objects.all())
    RequestConfig(request).configure(epgtable)
    return render(request, 'nxos_config_import/epgs.html', {'table': epgtable})

def epgs_form_data(request):
    epgformtable = epg_form_table(EpgInputForm.objects.all())
    RequestConfig(request).configure(epgformtable)
    return render(request, 'nxos_config_import/epgs_form.html', {'table': epgformtable})


def epg_new(request):
    if request.method == "POST":
        form = EpgForm(request.POST)
        if form.is_valid():
            for i in EpgInputForm.objects.all():
                i.delete()
            post = form.save(commit=False)
            #post.name = request.user
            #post.published_date = timezone.now()
            post.save()
            for i in EpgInputForm.objects.all():
                for epg in FvAEPg.objects.all():
                    epg = FvAEPg(
                        apic_addr=i.apic_addr,
                        encap=epg.encap,
                        legacy_switch=epg.legacy_switch,
                        vrf=epg.vrf,
                        pcEnfPref='unenforced',
                        dn='uni/tn-{}/ap-{}-LEGACY-{}_AP/epg-{}'.format(i.default_tenant, epg.vrf,
                                                                               epg.legacy_switch, epg.name),
                        name=epg.name,
                        tenant=i.default_tenant,
                        bd_tDn='uni/tn-{}/BD-{}-{}'.format(i.default_tenant, epg.encap, epg.name),
                        fvRsDomAtt_tDn='uni/phys-{}'.format(i.physical_domain),
                        fvRsPathAtt='topology/pod-1/protpaths-101-102/pathep-[IPG-{}]'.format(i.default_ipg_name)
                    )
                    epg.save()
            return HttpResponseRedirect('/nxos_config_import/epgs_form/')

    else:
        form = EpgForm()
    return render(request, 'nxos_config_import/home.html', {'form': form})
'''
def epg_new(request):
    form = EpgForm()
    return render(request, 'nxos_config_import/home.html', {'form': form})
'''
'''
def epg_form(request, pk):
    epg_instance = get_object_or_404(FvAEPg, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = EpgForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            for epg in FvAEPg.objects.all():
                epg.tenant = form.clean_tenant['tenant']
                epg.dn = 'uni/tn-{}/ap-DEFAULT-LEGACY-{}_AP/epg-{}'.format(form.clean_tenant['tenant'],
                                                                           epg.vrf, epg.name)
                epg.apic_addr = form.clean_apic_addr['apic_addr']
                epg.fvRsDomAtt_tDn = 'uni/phys-{}',format(form.clean_physical_domain['physical_domain'])

                epg.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('epgs') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = EpgForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': epg_instance,
    }

    return render(request, 'nxos_config_import/home.html', context)
'''
