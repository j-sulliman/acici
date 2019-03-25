from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse

from .models import Nxos_vlan_svi, FvAEPg, EpgInputForm, PushDataApic, ObjectConfigurationStatus
from.models import Document
from .tables import vlan_table, epg_table, epg_form_table, ObjectConfigurationTable
from .forms import EpgForm, PushDataForm, DocumentForm
from .aci_models.aci_requests import aci_post
from .aci_models.tenant_policy import fvTenant, fvAp, fvBD

from .misc_scripts import create_vlans_from_nxos, import_nxos_to_django, read_nxos_config_file, convert_vlans_to_epgs

from .misc_scripts import handle_uploaded_file
from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.contrib import messages





from django.contrib.auth.decorators import login_required


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', {'documents': documents})


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


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        config_file = read_nxos_config_file(fs.path(filename))
        imported_config = create_vlans_from_nxos(config_file)
        import_nxos_to_django(imported_config)
        convert_vlans_to_epgs()
        return render(request, 'nxos_config_import/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'nxos_config_import/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'nxos_config_import/model_form_upload.html', {
        'form': form
    })


def epg_new(request):
    saved = False
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
                        fvRsPathAtt=i.default_ipg_name,
                        mode=i.bd_mode,
                        fvSubnet=epg.fvSubnet
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
            object_dict["bd"] = []
            for i in PushDataApic.objects.all():
                for epg in FvAEPg.objects.all():
                    tenant_data = fvTenant(
                        name=epg.tenant, descr="Created by NXOS Config Generator",
                    )
                    if epg.tenant not in object_dict["tenants"]:
                        aci_post(apic_url=i.apic_addr,
                                 apic_user=i.user,
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

                        if epg.mode != 'l3' or epg.fvSubnet == 'DEFAULT':
                            bd_data = fvBD(name=epg.bd_tDn,
                                           description='L2 BD Created by NXOS Config Generator',
                                           tenant=epg.tenant,
                                           vrf=epg.vrf,
                                           arpFlood='yes',
                                           L2Unk_Unicast='flood',
                                           L3Unk_Mcast='flood',
                                           mcastAllow='no',
                                           MultiDest_Flood='bd-flood',
                                           EP_learn='no',
                                           EP_Move='',
                                           Limit_IP_Learn='yes',
                                           unicast_routing='no'
                                           )

                        elif epg.mode == 'l3' or epg.mode == 'L3' and epg.fvSubnet != 'DEFAULT':
                            bd_data = fvBD(name=epg.bd_tDn,
                                           description='L3 BD Created by NXOS Config Generator',
                                           tenant=epg.tenant,
                                           vrf=epg.vrf,
                                           arpFlood='no',
                                           L2Unk_Unicast='proxy',
                                           L3Unk_Mcast='opt-flood',
                                           mcastAllow='no',
                                           MultiDest_Flood='encap-flood',
                                           EP_learn='no',
                                           EP_Move='',
                                           Limit_IP_Learn='yes',
                                           unicast_routing='yes'
                                           )
                            bd_data.fvSubnet(subnet=epg.fvSubnet, scope='public',
                                             description='Created by NXOS Config Generator')



                        try:
                            json_bd_data = aci_post(apic_url=i.apic_addr,
                                                    apic_user="admin",
                                                    apic_pw=i.password,
                                                    mo_dn="node/mo/uni.json",
                                                    mo="fvBD",
                                                    mo_data=bd_data)


                            bd_config = ObjectConfigurationStatus(
                                object_name=epg.bd_tDn,
                                post_url=json_bd_data[2],
                                object_configuration=json_bd_data[0],
                                post_status=json_bd_data[1])
                            bd_config.save()

                            json_data = aci_post(apic_url=i.apic_addr,
                                     apic_user="admin",
                                     apic_pw=i.password,
                                     mo_dn="node/mo/uni.json",
                                     mo="fvAp",
                                     mo_data=epg_data)
                            #print(type(json_data))

                            # print(type(json_data))
                            config = ObjectConfigurationStatus(
                                object_name=epg.name,
                                post_url=json_data[2],
                                object_configuration=json_data[0],
                                post_status=json_data[1])
                            config.save()

                        except:
                            messages.add_message(request, messages.INFO,
                                'FAILED Posting object: {} - check configuration and connectivity'.format(epg.name))
                        '''
                        try:
                            json_data = aci_post(apic_url=i.apic_addr,
                                     apic_user="admin",
                                     apic_pw=i.password,
                                     mo_dn="node/mo/uni.json",
                                     mo="fvBd",
                                     mo_data=bd_data)
                            #print(type(json_data))
                            config = ObjectConfigurationStatus(
                                object_name=epg.bd_tDn,
                                post_url=json_data[2],
                                object_configuration =json_data[0],
                                post_status=json_data[1])
                            config.save()
                        except:
                            messages.add_message(request, messages.INFO,
                                'FAILED Posting object: {} - check configuration and connectivity'.format(epg.name))
                        '''


            return HttpResponseRedirect('/nxos_config_import/configuration/')

    else:
        form = EpgForm()
        form2 = PushDataForm()

    return render(request, 'nxos_config_import/home.html', {'form': form, 'form2': form2})


