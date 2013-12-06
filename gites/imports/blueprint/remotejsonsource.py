# -*- coding: utf-8 -*-
from zope.component import getUtility
from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection

from affinitic.pwmanager.interfaces import IPasswordManager


class RemoteJsonSourceSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.url = options.get('url')
        if self.url is None:
            raise ValueError('URL option is missing in %s section' % name)
        pwManager = getUtility(IPasswordManager, 'plone')
        self.user_id, self.password = pwManager.getLoginPass()
        self.data = self._get_data()

    def _get_data(self):
        import os
        import gites.imports
        folder = os.path.abspath(os.path.join(gites.imports.__file__, '../'))
        jsonFilePath = os.path.join(folder, 'packages.json')
        jsonFile = open(jsonFilePath, 'r')
        import anyjson
        data = anyjson.deserialize(jsonFile.read())
        jsonFile.close()
        return data
        # login_page = requests.post('http://localhost:5080/plone1/login',
        #                            data={'__ac_name': self.user_id,
        #                                  '__ac_password': self.password,
        #                                  'form.submitted': '1'})
        # private_page = requests.get(self.url,
        #                             cookies=login_page.cookies)
        # data = private_page.json()
        # if not isinstance(data, list):
        #     raise ValueError('json data has to be a list of dictionaries, got %s' % type(self.data))
        # return data

    def __iter__(self):
        for item in self.previous:
            yield item
        for item in self.data:
            if not isinstance(item, dict):
                raise ValueError('json data has to be a list of dictionaries, got %s' % type(item))
            yield item
