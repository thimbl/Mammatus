"""
Mammatus, a DNS-centric HA platform 

Dmytri Kleiner <dk@telekommunisten.net>, 2010
"""

import os, socket, urlparse
from twisted.internet import reactor
from twisted.internet.task import deferLater
from twisted.names import dns, common

class MammatusDnsResolver(common.ResolverBase):
    def setModel(self, model):
        self.model = model
    def _lookup(self, name, cls, type, timeout):
        queryType = dns.QUERY_TYPES[type]
        if hasattr(self, queryType):
            lookup = getattr(self, queryType)
            return lookup(name, type, timeout)
        else:
            def resolve():
                return ([], [], [])
            d = deferLater(reactor, 0, resolve)
            return d

class Controller(MammatusDnsResolver):
    def A(self, name, cls, timeout):
        def resolve(addr):
            RecordA = dns.Record_A(addr)
            RR = dns.RRHeader(name=name,cls=cls,type=dns.A,ttl=60,payload=RecordA)
            return ([RR], [], [])
        d = deferLater(reactor, 0, self.model.getHostByName, name)
        d.addCallback(resolve)
        return d
def getController(model):
    controller = Controller()
    controller.setModel(model)
    return controller

