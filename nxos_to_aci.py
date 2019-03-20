import os
import json
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
        if line.startswith(cmd_string) and len(line) < 11:
            prev_line = line
            temp_line = line.split(" ")
            vlan_id = temp_line[1].strip()
            epgs_bds[vlan_id] = {}
        elif line.startswith("  name") and prev_line.startswith(cmd_string):
            vlan_name_lst = line.split("  name")
            vlan_name = vlan_name_lst[1].strip()
            epgs_bds[vlan_id]= {
                "name": vlan_name}
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

config_file = read_nxos_config_file()
epgs_bds = create_vlans_from_nxos(config_file)
for keys, values in epgs_bds.items():
    vlan_entry = Nxos_vlan_svi(
        encap=keys,
        name=values.get("name"),
        svi_ip=values.get("ip", "DEFAULT"),
        vrf=values.get("vrf", "DEFAULT")
    )
    print("encap: {} name: {}, ip {}, vrf {} ".format(keys, values.get("name"), values.get("ip"), values.get("vrf")))
    vlan_entry.save()
'''
for keys, values in epgs_bds.items():
    try:
        print("found")
        print(keys)
        fvBD_entry = FvBD(apic_addr="192.168.0.1",
                          descr=epgs_bds[keys]["name"],
                          dn="uni/tn-LEGACY_DEFAULT/BD-{}".format(epgs_bds[keys]["name"]),
                          arpFlood="yes",
                          epMoveDetectMode="",
                          ipLearning="no",
                          limitIpLearnToSubnets="yes",
                          name=epgs_bds[keys]["name"],
                          unicastRoute="yes",
                          unkMacUcastAct="flood",
                          unkMcastAct="flood",
                          fvSubnet1=epgs_bds[keys]["ip"],
                          fvSubnet1_scope="public",
                          fvRsCtx=epgs_bds[keys]["vrf"]
                        )
    except KeyError:
        fvBD_entry = FvBD(apic_addr="192.168.0.1",
                          descr=epgs_bds[keys]["name"],
                          dn="uni/tn-LEGACY_DEFAULT/BD-{}".format(epgs_bds[keys]["name"]),
                          arpFlood="yes",
                          epMoveDetectMode="",
                          ipLearning="no",
                          limitIpLearnToSubnets="yes",
                          name=epgs_bds[keys]["name"],
                          unicastRoute="yes",
                          unkMacUcastAct="flood",
                          unkMcastAct="flood",
                          fvSubnet1="none",
                          fvSubnet1_scope="public",
                          fvRsCtx=epgs_bds[keys]["vrf"]
                          )
        print("not found")
'''

#print(json.dumps(epgs_bds, sort_keys=True, indent=4))