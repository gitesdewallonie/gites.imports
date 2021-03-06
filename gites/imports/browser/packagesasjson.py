# -*- coding: utf-8 -*-
import base64
import json
import os
from Acquisition import aq_base
from Products.Archetypes import BaseUnit
from Products.Archetypes.Field import Image
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import getToolByName
from DateTime import DateTime
from plone.app.blob.field import BlobWrapper
from zope.component import getMultiAdapter
from gites.core.interfaces import IHebergementsFetcher

#: Private attributes we add to the export list
EXPORT_ATTRIBUTES = ["portal_type", "id"]

EXCLUDE_FIELDS = ["largePhoto"]

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

        elif isinstance(value, BlobWrapper) or isinstance(value, Image):
            if not EXPORT_BINARY:
                return None
            if hasattr(value, 'data'):
                data = str(getattr(value, 'data'))
            else:
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
            if name in EXCLUDE_FIELDS:
                continue
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
        contentFilter['effectiveRange'] = DateTime()
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

    def get_all_content(self, roomsOnly=True):
        for package in self.get_all_packages():
            hebs = list(self.getHebergementIdsForPackages(package, roomsOnly))
            if not hebs:
                continue
            yield package
            for image in self.get_package_images(package):
                yield image

    def getHebergementIdsForPackages(self, package, roomsOnly=False):
        fetcher = getMultiAdapter((package, self,
                                  self.request),
                                  IHebergementsFetcher)
        for heb in fetcher():
            if roomsOnly and heb.type.type_heb_type == 'gite':
                continue
            yield heb.heb_pk

    def export(self, roomsOnly=False):
        array = []
        portal_url = getToolByName(self.context, 'portal_url')
        for obj in self.get_all_content(roomsOnly):
            data = self.grabArchetypesData(obj)
            data.update(self.grabAttributes(obj))
            data['path'] = portal_url.getRelativeContentURL(obj)
            data['uid'] = aq_base(obj).UID()
            if obj.isCanonical():
                data['isCanonical'] = True
                data['canonical'] = data['path']
            else:
                data['isCanonical'] = False
                canonicalObj = obj.getCanonical()
                data['canonical'] = portal_url.getRelativeContentURL(canonicalObj)
            data['type'] = obj.portal_type
            if obj.portal_type == 'Package':
                hebs = list(self.getHebergementIdsForPackages(obj, roomsOnly))
                data['hebergements'] = hebs
            if obj.portal_type in ['Image', 'Vignette']:
                mime_type = obj.getField('image').getContentType(obj)
                data['_image_mimetype'] = mime_type
            array.append(data)
        return array

    def __call__(self):
        request = self.request
        roomsOnly = request.get('roomsOnly', False)
        data = self.export(roomsOnly)
        sortOrder = {'Package': 1, 'Image': 2, 'Vignette': 3}
        data.sort(key=lambda x: sortOrder[x['portal_type']])
        pretty = json.dumps(data)
        self.request.response.setHeader("Content-type", "application/json")
        return pretty
