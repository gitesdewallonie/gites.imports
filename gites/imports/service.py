# -*- coding: utf-8 -*-
from zope.component import getUtilitiesFor
from zope.component.hooks import getSite
from OFS.event import ObjectWillBeRemovedEvent
from OFS.interfaces import IObjectWillBeMovedEvent
import grokcore.component as grok
from five.taskqueue.service import TaskService
from Products.CMFPlone.interfaces import IPloneSiteRoot
from z3c.taskqueue.interfaces import ITaskService
from z3c.taskqueue import task
from collective.transmogrifier.interfaces import ITransmogrifier


def sync_packages(input):
    site = getSite()
    transmogrifier = ITransmogrifier(site)
    transmogrifier('packages')

syncPackagesTask = task.SimpleTask(sync_packages)


class Service(TaskService):

    def __init__(self):
        super(Service, self).__init__()
        self.addCronJob(u'sync-packages', (), minute=10)


@grok.subscribe(IPloneSiteRoot, IObjectWillBeMovedEvent)
def stopAllTaskServices(wiwoApp, event):
    if event is None or event.__class__ == ObjectWillBeRemovedEvent:
        for name, service in getUtilitiesFor(ITaskService, context=wiwoApp):
            service.stopProcessing()
