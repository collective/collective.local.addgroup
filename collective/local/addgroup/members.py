from Acquisition import aq_inner
from zope.component import getAdapter

from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.security import ISecuritySchema
from plone.app.controlpanel.usergroups import GroupMembershipControlPanel


class ManageMembers(GroupMembershipControlPanel):

    @property
    def email_as_username(self):
        portal = getToolByName(aq_inner(self.context), 'portal_url').getPortalObject()
        return getAdapter(portal, ISecuritySchema).get_use_email_as_login()

