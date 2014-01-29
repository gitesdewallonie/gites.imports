# -*- coding: utf-8 -*-

from collective.transmogrifier.transmogrifier import Transmogrifier
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser

import transaction


def deleteAllIdeesSejours(portal):
    ideesSejoursFolder = getattr(portal, 'idee-sejour')
    for objId in ideesSejoursFolder.contentIds():
        ideesSejoursFolder.manage_delObjects(objId)


def main(app):
    portal = app.unrestrictedTraverse("plone1")
    sm = getSecurityManager()
    user = UnrestrictedUser('script', '', ['Manager'], '')
    user = user.__of__(portal.acl_users)
    newSecurityManager(None, user)

    deleteAllIdeesSejours(portal)

    transmogrifier = Transmogrifier(portal)
    transmogrifier(u'gites.import.packages')
    setSecurityManager(sm)
    transaction.commit()


if "app" in locals():
    main(app)
