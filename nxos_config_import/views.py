from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Nxos_vlan_svi, FvAEPg, EpgInputForm, PushDataApic, ObjectConfigurationStatus
from .tables import vlan_table, epg_table, epg_form_table, ObjectConfigurationTable
from .forms import EpgForm, PushDataForm
from .aci_models.aci_requests import aci_post
from .aci_models.tenant_policy import fvTenant, fvAp


from django.contrib import messages





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


def object_config_data(request):
    objecttable = ObjectConfigurationTable(ObjectConfigurationStatus.objects.all())
    RequestConfig(request).configure(objecttable)
    return render(request, 'nxos_config_import/configuration.html', {'table': objecttable})


def epg_new(request):
    if request.method == "POST":
        form = EpgForm(request.POST)
        form2 = PushDataForm(request.POST)
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
                        bd_tDn='{}_BD'.format(epg.name[0:-4]),
                        fvRsDomAtt_tDn=i.physical_domain,
                        fvRsPathAtt=i.default_ipg_name
                    )
                    epg.save()
            return HttpResponseRedirect('/nxos_config_import/epgs_form/')

        if form2.is_valid():
            for i in PushDataApic.objects.all():
                i.delete()
            post2 = form2.save(commit=False)
            #post.name = request.user
            #post.published_date = timezone.now()
            post2.save()
            object_dict = {}
            object_dict["tenants"] = []
            object_dict["epgs"] = []
            for i in PushDataApic.objects.all():
                for epg in FvAEPg.objects.all():
                    tenant_data = fvTenant(
                        name=epg.tenant, descr="Created by NXOS Config Generator",
                    )
                    if epg.tenant not in object_dict["tenants"]:
                        aci_post(apic_url=i.apic_addr,
                                 apic_user="admin",
                                 apic_pw=i.password,
                                 mo_dn="node/mo/uni.json",
                                 mo="fvTenant",
                                 mo_data=tenant_data)
                        object_dict["tenants"].append(epg.tenant)
                    if epg.name not in object_dict["epgs"]:
                        epg_data = fvAp(tenant=epg.tenant,
                                        ap_name='DEFAULT-LEGACY-{}_AP'.format(epg.legacy_switch),
                                        ap_description='Created by NXOS Config Generator',
                                        epg_description='Created by NXOS Config Generator',
                                        epg_name=epg.name,
                                        isAttrBasedEPg='no',
                                        pcEnfPref='unenforced',
                                        prefGrMemb='exclude')
                        epg_data.fvRsBd(associated_bd=epg.bd_tDn)
                        epg_data.fvRsDomAtt(phydom=epg.fvRsDomAtt_tDn)
                        epg_data.fvRsPathAtt(encap=epg.encap, tDn=epg.fvRsPathAtt,
                                             path_desc='Created by NXOS Config Generator')

                        try:
                            json_data = aci_post(apic_url=i.apic_addr,
                                     apic_user="admin",
                                     apic_pw=i.password,
                                     mo_dn="node/mo/uni.json",
                                     mo="fvAp",
                                     mo_data=epg_data)
                            #print(type(json_data))
                            config = ObjectConfigurationStatus(
                                object_name = epg.name,
                                post_url = json_data[2],
                                object_configuration = json_data[0],
                                post_status = json_data[1])
                            config.save()
                        except:
                            messages.add_message(request, messages.INFO,
                                'FAILED Posting object: {} - check configuration and connectivity'.format(epg.name))

            return HttpResponseRedirect('/nxos_config_import/configuration/')

    else:
        form = EpgForm()
        form2 = PushDataForm()
    return render(request, 'nxos_config_import/home.html', {'form': form, 'form2': form2})


