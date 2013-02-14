# -*- coding: utf-8 -*-
from zope.component import getUtilitiesFor
from OFS.event import ObjectWillBeRemovedEvent
from OFS.interfaces import IObjectWillBeMovedEvent
import grokcore.component as grok
from five.taskqueue.service import TaskService
from Products.CMFPlone.interfaces import IPloneSiteRoot
from z3c.taskqueue.interfaces import ITaskService


class Service(TaskService):

    def __init__(self):
        super(Service, self).__init__()
        self.addCronJob(u'sync-packages', (), minute=10)


@grok.subscribe(IPloneSiteRoot, IObjectWillBeMovedEvent)
def stopAllTaskServices(wiwoApp, event):
    if event is None or event.__class__ == ObjectWillBeRemovedEvent:
        for name, service in getUtilitiesFor(ITaskService, context=wiwoApp):
            service.stopProcessing()
