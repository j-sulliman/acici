from django.db import models
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
    pcEnfPref = models.CharField(max_length=200)
    dn = models.CharField(max_length=200)
    name = models.CharField(primary_key=True, max_length=200)
    tenant = models.CharField(default='none', max_length=200)
    encap = models.CharField(default='none', max_length=200)
    legacy_switch = models.CharField(default='none', max_length=200)
    bd_tDn = models.CharField(max_length=200)
    fvRsDomAtt_tDn = models.CharField(max_length=200)
    fvRsPathAtt = models.CharField(max_length=200)
    vzAny = models.CharField(max_length=3, default='yes')
    mode = models.CharField(max_length=2, default='l2')
    vrf = models.CharField(default='none', max_length=200)
    fvSubnet = models.GenericIPAddressField(max_length=200)
    modTs = models.CharField(max_length=200)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.dn


class FvBD(models.Model):
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
    fvSubnet1 = models.CharField(max_length=200)
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
        return self.dn


class EpgInputForm(models.Model):
    apic_addr = models.GenericIPAddressField(primary_key=True, max_length=200,
                                             default='sandboxapicdc.cisco.com')
    default_tenant = models.CharField(max_length=200, default='LEGACY-TENANT-TN')
    default_ipg_name = models.CharField(max_length=200, default='LEGACY-NEXUS-VPC_IPG')
    physical_domain = models.CharField(max_length=200, default='LEGACY_PHY')
    migration_leafs_nodeid = models.CharField(max_length=200, default='101-102')
    bd_mode = models.CharField(max_length=200, default='l2')

    def __str__(self):
        return self.apic_addr


class PushDataApic(models.Model):
    apic_addr = models.CharField(primary_key=True, max_length=200, default='sandboxapicdc.cisco.com')
    user = models.CharField(default='admin', max_length=200)
    password = models.CharField(default='ciscopsdt', max_length=200)

    def __str__(self):
        return self.apic_addr


class ObjectConfigurationStatus(models.Model):
    object_name = models.CharField(primary_key=True, max_length=200)
    object_configuration = models.TextField()
    post_url = models.URLField(default='none')
    post_status = models.CharField(max_length=200)
    post_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.object_name


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
