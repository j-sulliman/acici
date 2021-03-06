import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'nxos_aci.settings'


import django
django.setup()
from nxos_config_import.models import FvAEPg, FvBD, Nxos_vlan_svi


def read_nxos_config_file(filename="Configurations/SW-ATCA-93180-1-Configuration_0.1"):
    config_file = open(filename, "r")
    return config_file

def create_vlans_from_nxos(file,  cmd_string="vlan "):
    vlan_id = ''
    prev_line = ''
    epgs_bds = {}
    vrf_lst = []
    for line in config_file:
        if line.startswith("hostname "):
            tmp_hostname = line.split("hostname ")
            hostname = tmp_hostname[1].strip()
        if line.startswith(cmd_string) and len(line) < 11:
            prev_line = line
            temp_line = line.split(" ")
            vlan_id = temp_line[1].strip()
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
            prev_line = line
        elif line.startswith("  vrf member") and prev_line.startswith('interface Vlan'):
            vrf_lst = line.split('  vrf member ')
            epgs_bds[svi_cleaned]["vrf"] = vrf_lst[1].strip()
        try:
            if line.startswith("  ip address") and prev_line.startswith('interface Vlan') and epgs_bds[svi_cleaned]["vrf"] == vrf_lst[1].strip():
                ip_lst = line.split('  ip address ')
                epgs_bds[svi_cleaned]['ip'] = ip_lst[1].strip()
        except:
            if line.startswith("  ip address") and prev_line.startswith('interface Vlan'):
                ip_lst = line.split('  ip address ')
            epgs_bds[svi_cleaned]["vrf"] = "DEFAULT"
            epgs_bds[svi_cleaned]["ip"] = ip_lst[1].strip()
    return epgs_bds


def import_nxos_to_django(input_dict):
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


config_file = read_nxos_config_file()
epgs_bds = create_vlans_from_nxos(config_file)
import_nxos_to_django(epgs_bds)
convert_vlans_to_epgs()


