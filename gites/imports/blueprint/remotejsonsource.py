# -*- coding: utf-8 -*-
import anyjson
import urllib
import urllib2
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
        self.view = options.get('view')
        if self.url is None:
            raise ValueError('URL option is missing in %s section' % name)
        if self.view is None:
            raise ValueError('View option is missing in %s section' % name)
        pwManager = getUtility(IPasswordManager, 'plone')
        self.user_id, self.password = pwManager.getLoginPass()
        self.data = self._get_data()
        # self.data = self._get_static_data()

    def _get_static_data(self):
        """
        For tests purpose
        """
        import os
        import gites.imports
        folder = os.path.abspath(os.path.join(gites.imports.__file__, '../'))
        jsonFilePath = os.path.join(folder, 'packages.json')
        jsonFile = open(jsonFilePath, 'r')
        data = anyjson.deserialize(jsonFile.read())
        jsonFile.close()
        return data

    def _get_data(self):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        urllib2.install_opener(opener)
        data = urllib.urlencode({'__ac_name': self.user_id,
                                 '__ac_password': self.password,
                                 'form.submitted': '1'})

        loginUrl = "%s/login" % self.url
        req = urllib2.Request(loginUrl, data)
        urllib2.urlopen(req)

        jsonUrl = "%s/%s" % (self.url, self.view)
        req = urllib2.Request(jsonUrl)
        jsonFile = urllib2.urlopen(req)
        data = anyjson.deserialize(jsonFile.read())
        return data

    def __iter__(self):
        for item in self.previous:
            yield item
        for item in self.data:
            if not isinstance(item, dict):
                raise ValueError('json data has to be a list of dictionaries, got %s' % type(item))
            yield item
