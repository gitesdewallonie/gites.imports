# -*- coding: utf-8 -*-
import base64
import json
import os

from Products.Archetypes import BaseUnit
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import getToolByName
from DateTime import DateTime
from plone.app.blob.field import BlobWrapper

#: Private attributes we add to the export list
EXPORT_ATTRIBUTES = ["portal_type", "id"]

#: Do we dump out binary data... default we do, but can be controlled with env var
EXPORT_BINARY = os.getenv("EXPORT_BINARY", None)
if EXPORT_BINARY:
    EXPORT_BINARY = EXPORT_BINARY == "true"
else:
    EXPORT_BINARY = True


class PackageAsJson(BrowserView):

    def convert(self, value):
        """
        Convert value to more JSON friendly format.
        """
        if isinstance(value, DateTime):
            # Zope DateTime
            # http://pypi.python.org/pypi/DateTime/3.0.2
            return value.ISO8601()

        elif isinstance(value, BlobWrapper):
            if not EXPORT_BINARY:
                return None
            data = str(value)
            if not data:
                return None
            return base64.b64encode(data)
        elif isinstance(value, BaseUnit.BaseUnit) and value.isBinary():

            if not EXPORT_BINARY:
                return None

            # Archetypes FileField and ImageField payloads
            # are binary as OFS.Image.File object
            data = getattr(value.data, "data", None)
            if not data:
                return None
            return base64.b64encode(data)
        else:
            # Passthrough
            return value

    def grabArchetypesData(self, obj):
        """
        Export Archetypes schemad data as dictionary object.

        Binary fields are encoded as BASE64.
        """
        data = {}
        for field in obj.Schema().fields():
            name = field.getName()
            value = field.getRaw(obj)
            data[name] = self.convert(value)
        return data

    def grabAttributes(self, obj):
        data = {}
        for key in EXPORT_ATTRIBUTES:
            data[key] = self.convert(getattr(obj, key, None))
        return data

    def get_all_packages(self):
        cat = getToolByName(self.context, 'portal_catalog')
        contentFilter = {}
        contentFilter['review_state'] = 'published'
        contentFilter['Language'] = 'all'
        contentFilter['portal_type'] = ['Package']
        for brain in cat(contentFilter):
            yield brain.getObject()

    def get_package_images(self, package):
        cat = getToolByName(self.context, 'portal_catalog')
        package_url = "/".join(package.getPhysicalPath())
        contentFilter = {}
        path = {}
        path['query'] = package_url
        path['depth'] = 2
        contentFilter['path'] = path
        contentFilter['portal_type'] = ['Vignette', 'Image']
        contentFilter['Language'] = 'all'
        for brain in cat(contentFilter):
            yield brain.getObject()

    def get_all_content(self):
        for package in self.get_all_packages():
            yield package
            for image in self.get_package_images(package):
                yield image

    def export(self):
        array = []
        portal_url = getToolByName(self.context, 'portal_url')
        for obj in self.get_all_content():
            data = self.grabArchetypesData(obj)
            data.update(self.grabAttributes(obj))
            data['path'] = portal_url.getRelativeContentURL(obj)
            data['type'] = obj.portal_type
            array.append(data)
        return array

    def __call__(self):
        data = self.export()
        pretty = json.dumps(data, sort_keys=True)
        self.request.response.setHeader("Content-type", "application/json")
        return pretty
