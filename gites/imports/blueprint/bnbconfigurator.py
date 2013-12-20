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

    def __iter__(self):
        for item in self.previous:
            if item['portal_type'] != 'Package':
                yield item
            item['type'] = 'IdeeSejour'
            item['portal_type'] = 'IdeeSejour'
            hebs = item['hebergements']
            strHebs = [str(heb) for heb in hebs]
            item['hebergements'] = strHebs
            item['transitions'] = 'publish'
            yield item
