# -*- coding: utf-8 -*-
import requests
from zope.component import getUtility
from zope.interface import classProvides, implements
from plone.registry.interfaces import IRegistry
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection


class RemoteJsonSourceSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.url = options.get('url')
        if self.url is None:
            raise ValueError('URL option is missing in %s section' % name)
        registry = getUtility(IRegistry, context=self.context)
        self.user_id = registry['gites.imports.packages.user_id']
        self.password = registry['gites.imports.packages.password']
        self.data = self._get_data()

    def _get_data(self):
        login_page = requests.post('http://localhost:5080/plone1/login',
                                   data={'__ac_name': self.user_id,
                                         '__ac_password': self.password,
                                         'form.submitted': '1'})
        private_page = requests.get(self.url,
                                    cookies=login_page.cookies)
        data = private_page.json()
        if not isinstance(data, list):
            raise ValueError('json data has to be a list of dictionaries, got %s' % type(self.data))
        return data

    def __iter__(self):
        for item in self.previous:
            yield item
        for item in self.data:
            if not isinstance(item, dict):
                raise ValueError('json data has to be a list of dictionaries, got %s' % type(item))
            yield item
