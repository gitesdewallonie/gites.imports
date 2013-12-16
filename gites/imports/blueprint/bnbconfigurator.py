# -*- coding: utf-8 -*-
from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection


class BNBConfiguratorSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.portalType = options.get('portal-type')

    def __iter__(self):
        for item in self.previous:
            item['type'] = self.portalType
            item['portal_type'] = self.portalType
            hebs = item['hebergements']
            strHebs = [str(heb) for heb in hebs]
            item['hebergements'] = strHebs
            item['transitions'] = 'publish'
            yield item
