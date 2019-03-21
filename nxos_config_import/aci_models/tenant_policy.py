class fvTenant:
 def __init__(self, name, descr):
     self.fvTenant = {
     'attributes' : {
     'dn' :"uni/tn-%s" % name,
     'descr' : descr,
     'name' : name }}


class fvCtx(object):
    def __init__(self, name, descr, tenant,pcenfpref, pcEnfDir):
        self.fvCtx = {
        'attributes' : {
        'dn' : "uni/tn-%s/ctx-%s" % (tenant, name),
        'knwMcastAct' : 'permit',
        'name' : name,
        'pcEnfDir' : pcEnfDir,
        'pcEnfPref' : pcenfpref}}
    #def name(self):
        #return self.fvCtx['attributes']['name']


class fvBD (object):
    def __init__(self, name, description, tenant, vrf,  arpFlood, L2Unk_Unicast,
     L3Unk_Mcast, mcastAllow, MultiDest_Flood, EP_learn, EP_Move, Limit_IP_Learn,
      unicast_routing):
        self.fvBD = {
         "attributes": {
                    "arpFlood": arpFlood,
                    "descr": description,
                    "dn": "uni/tn-%s/BD-%s" % (tenant, name),
                    "epMoveDetectMode": EP_Move,
                    "ipLearning": EP_learn,
                    "limitIpLearnToSubnets": Limit_IP_Learn,
                    "llAddr": "::",
                    "mcastAllow": mcastAllow,
                    "multiDstPktAct": MultiDest_Flood,
                    "name": name,
                    "ownerKey": "",
                    "ownerTag": "",
                    "type": "regular",
                    "unicastRoute": unicast_routing,
                    "unkMacUcastAct": L2Unk_Unicast,
                    "unkMcastAct": L3Unk_Mcast,
                    "vmac": "not-applicable"
                },
                "children": [
                    {
                        "fvRsBDToNdP": {
                            "attributes": {
                                "tnNdIfPolName": ""
                            }
                        }
                    },
                    {
                        "fvRsCtx": {
                            "attributes": {
                                "tnFvCtxName": vrf
                            }
                        }
                    },
                    {
                        "fvRsIgmpsn": {
                            "attributes": {
                                "tnIgmpSnoopPolName": ""
                            }
                        }
                    },
                    {
                        "fvRsBdToEpRet": {
                            "attributes": {
                                "resolveAct": "resolve",
                                "tnFvEpRetPolName": ""
                            }
                        }
                    }
                ]
            }

    #@classmethod
    def fvSubnet(self, subnet, scope, description = ''):
        fvSubnet = {
        'fvSubnet' : {
        'attributes' : {
        "ctrl": "",
        "descr": description,
        "ip": subnet,
        "name": "",
        "scope": scope,
        "virtual": "no"
        }
        }
        }
        self.fvBD['children'].append(fvSubnet)

    def fvRsBDToOut(self, L3O_name):
        fvRsBDToOut = {
                "fvRsBDToOut": {
                                "attributes": {
                                    "tnL3extOutName": L3O_name
                                    }
                                }
                        }
        self.fvBD['children'].append(fvRsBDToOut)


class fvAp (object):
    def __init__(self, tenant, ap_name, ap_description, epg_description, epg_name,
       isAttrBasedEPg = 'no', pcEnfPref ='unenforced', prefGrMemb = 'exclude'):
        self.fvAp = {
            "attributes": {
              "descr": ap_description,
              "dn": "uni/tn-%s/ap-%s" % (tenant, ap_name),
              "name": ap_name,
              "ownerKey": "",
              "ownerTag": "",
              "prio": "unspecified"
            },
            "children": [
              {
                "fvAEPg": {
                  "attributes": {
                    "descr": epg_description,
                    "fwdCtrl": "",
                    "isAttrBasedEPg": isAttrBasedEPg,
                    "matchT": "AtleastOne",
                    "name": epg_name,
                    "pcEnfPref": pcEnfPref,
                    "prefGrMemb": prefGrMemb,
                    "prio": "unspecified"
                  },
                  "children": [
                  ]
                        }
                }
            ]
            }

    def fvRsPathAtt(self, encap, path_desc, tDn, instrImedcy = 'lazy'):
        fvRsPathAtt = {
        "fvRsPathAtt": {
          "attributes": {
            "descr": path_desc,
            "encap": "vlan-%s" % encap,
            "instrImedcy": instrImedcy,
            "mode": "regular",
            "primaryEncap": "unknown",
            "tDn": tDn
          }
        }
        }
        self.fvAp['children'][0]['fvAEPg']['children'].append(fvRsPathAtt)

    def fvRsDomAtt(self, phydom):
        fvRsDomAtt = {
        "fvRsDomAtt": {
          "attributes": {
            "classPref": "encap",
            "delimiter": "",
            "encap": "unknown",
            "encapMode": "auto",
            "epgCos": "Cos0",
            "epgCosPref": "disabled",
            "instrImedcy": "lazy",
            "netflowDir": "both",
            "netflowPref": "disabled",
            "primaryEncap": "unknown",
            "resImedcy": "immediate",
            "tDn": "uni/phys-%s" % phydom
          }
        }
        }
        self.fvAp['children'][0]['fvAEPg']['children'].append(fvRsDomAtt)


    def fvRsCustQosPol(self, qos_pol = 'default'):
        fvRsCustQosPol = {
        "fvRsCustQosPol": {
          "attributes": {
            "tnQosCustomPolName": qos_pol
          }
        }
        }
        self.fvAp['children'][0]['fvAEPg']['children'].append(fvRsCustQosPol)

    def fvRsBd(self, associated_bd):
        fvRsBd = {
        "fvRsBd": {
          "attributes": {
            "tnFvBDName": associated_bd
            }
            }
            }
self.fvAp['children'][0]['fvAEPg']['children'].append(fvRsBd)