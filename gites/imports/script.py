# -*- coding: utf-8 -*-

from collective.transmogrifier.transmogrifier import Transmogrifier
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser

import transaction


def main(app):
    portal = app.unrestrictedTraverse("plone1")
    sm = getSecurityManager()
    user = UnrestrictedUser('script', '', ['Manager'], '')
    user = user.__of__(portal.acl_users)
    newSecurityManager(None, user)

    transmogrifier = Transmogrifier(portal)
    transmogrifier(u'gites.import.packages')
    setSecurityManager(sm)
    transaction.commit()


if "app" in locals():
    main(app)
