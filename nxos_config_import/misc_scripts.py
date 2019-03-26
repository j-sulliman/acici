from .models import FvAEPg, Nxos_vlan_svi
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'nxos_aci.settings'


import django
django.setup()


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def read_nxos_config_file(filename="Configurations/SW-ATCA-93180-1-Configuration_0.1"):
    config_file = open(filename, "r")
    return config_file


def create_vlans_from_nxos(file,  cmd_string="vlan "):
    vlan_id = ''
    prev_line = ''
    epgs_bds = {}
    vrf_lst = []
    for line in file:
        if line.startswith("hostname "):
            tmp_hostname = line.split("hostname ")
            hostname = tmp_hostname[1].strip()
        if line.startswith(cmd_string) and len(line) < 11:
            prev_line = line
            temp_line = line.split(" ")
            vlan_id = temp_line[1].strip()
            if len(vlan_id) == 1:
                vlan_id = '000' + vlan_id
            elif len(vlan_id) == 2:
                vlan_id = '00'+ vlan_id
            elif len(vlan_id) == 3:
                vlan_id = '0' + vlan_id
            epgs_bds[vlan_id] = {}
        elif line.startswith("  name") and prev_line.startswith(cmd_string):
            vlan_name_lst = line.split("  name")
            vlan_name = vlan_name_lst[1].strip()
            epgs_bds[vlan_id]= {
                "name": vlan_name,
                "hostname": hostname}
        elif line.startswith("interface Vlan"):
            subnet_lst = line.split('interface Vlan')
            svi_cleaned = subnet_lst[1].strip()
            if len(svi_cleaned) == 1:
                svi_cleaned = '000' + svi_cleaned
            elif len(svi_cleaned) == 2:
                svi_cleaned = '00'+ svi_cleaned
            elif len(svi_cleaned) == 3:
                svi_cleaned = '0' + svi_cleaned
            prev_line = line
        elif line.startswith("  vrf member") and prev_line.startswith('interface Vlan'):
            vrf_lst = line.split('  vrf member ')
            if svi_cleaned in epgs_bds.keys():
                epgs_bds[svi_cleaned]["vrf"] = vrf_lst[1].strip()
        try:
            if line.startswith("  ip address") and prev_line.startswith('interface Vlan') and epgs_bds[svi_cleaned]["vrf"] == vrf_lst[1].strip():
                ip_lst = line.split('  ip address ')
                epgs_bds[svi_cleaned]['ip'] = ip_lst[1].strip()
        except:
            if line.startswith("  ip address") and prev_line.startswith('interface Vlan'):
                ip_lst = line.split('  ip address ')
            if svi_cleaned in epgs_bds.keys():
                epgs_bds[svi_cleaned]["vrf"] = "DEFAULT"
                epgs_bds[svi_cleaned]["ip"] = ip_lst[1].strip()
    return epgs_bds


def import_nxos_to_django(input_dict):
    Nxos_vlan_svi.objects.all().delete()
    for keys, values in input_dict.items():
        vlan_entry = Nxos_vlan_svi(
            encap=keys,
            name=values.get("name").upper(),
            svi_ip=values.get("ip", "DEFAULT"),
            vrf=values.get("vrf", "DEFAULT").upper(),
            hostname=values.get("hostname", "DEFAULT").upper()
        )
        vlan_entry.save()


def convert_vlans_to_epgs():
    FvAEPg.objects.all().delete()
    vlan_len = len(Nxos_vlan_svi.objects.all())
    for vlan in Nxos_vlan_svi.objects.all():
        print("vlan: {} name: {}".format(vlan.encap, vlan.name))
        epg = FvAEPg(
            apic_addr='192.168.0.1',
            pcEnfPref='unenforced',
            dn='uni/tn-NXOS-ACI-DEFAULT/ap-{}-LEGACY-{}_AP/epg-{}-{}_EPG'.format(vlan.vrf, vlan.hostname, vlan.encap,
                                                                                 vlan.name),
            name='{}-{}_EPG'.format(vlan.encap, vlan.name),
            tenant='NXOS-ACI-DEFAULT',
            bd_tDn ='BD-{}-{}_BD'.format(vlan.encap, vlan.name),
            fvRsDomAtt_tDn='LEGACY_PHY',
            fvRsPathAtt='IPG-LEGACY-{}_IPG'.format(vlan.hostname),
            encap=vlan.encap,
            legacy_switch=vlan.hostname,
            vrf=vlan.vrf,
            fvSubnet=vlan.svi_ip
        )
        epg.save()
    return vlan_len


#convert_vlans_to_epgs()

