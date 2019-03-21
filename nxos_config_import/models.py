from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Nxos_vlan_svi(models.Model):
    encap = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(default='none', max_length=200)
    svi_ip = models.CharField(default='none', max_length=200)
    vrf = models.CharField(default='none', max_length=200)
    hostname = models.CharField(default='none', max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class FvAEPg(models.Model):
    apic_addr = models.CharField(max_length=200)
    pcEnfPref = models.CharField(max_length=200)
    dn = models.CharField(max_length=200)
    name = models.CharField(primary_key=True, max_length=200)
    tenant = models.CharField(default='none', max_length=200)
    encap = models.CharField(default='none', max_length=200)
    legacy_switch = models.CharField(default='none', max_length=200)
    bd_tDn = models.CharField(max_length=200)
    fvRsDomAtt_tDn = models.CharField(max_length=200)
    fvRsPathAtt = models.CharField(max_length=200)
    fvRsCons = models.CharField(max_length=200)
    fvRsProv = models.CharField(max_length=200)
    vrf = models.CharField(default='none', max_length=200)
    modTs = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.apic_addr


class FvBD(models.Model):
    apic_addr = models.CharField(max_length=200)
    descr = models.CharField(max_length=200)
    dn = models.CharField(primary_key=True, max_length=200)
    arpFlood = models.CharField(max_length=200)
    epMoveDetectMode = models.CharField(max_length=200)
    ipLearning = models.CharField(max_length=200)
    limitIpLearnToSubnets = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    unicastRoute = models.CharField(max_length=200)
    unkMacUcastAct = models.CharField(max_length=200)
    unkMcastAct = models.CharField(max_length=200)
    fvSubnet1 = models.CharField(max_length=200, default='none')
    fvSubnet1_scope = models.CharField(max_length=200, default='none')
    fvSubnet2 = models.CharField(max_length=200, default='none')
    fvSubnet2_scope = models.CharField(max_length=200, default='none')
    fvSubnet3 = models.CharField(max_length=200,  default='none')
    fvSubnet3_scope = models.CharField(max_length=200, default='none')
    fvRsCtx = models.CharField(max_length=200, default='none')
    fvRsBDToOut1 = models.CharField(max_length=200, default='none')
    fvRsBDToOut2 = models.CharField(max_length=200, default='none')
    fvRsBDToOut3 = models.CharField(max_length=200, default='none')
    modTs = models.CharField(max_length=200, default='none')
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.apic_addr


class EpgInputForm(models.Model):
    apic_addr = models.CharField(primary_key=True, max_length=200)
    default_tenant = models.CharField(max_length=200)
    default_ipg_name = models.CharField(max_length=200)
    physical_domain = models.CharField(max_length=200)

    def __str__(self):
        return self.apic_addr
