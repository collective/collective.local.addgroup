from zope.component import getUtility

from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from collective.local.addgroup.interfaces import IAddNewGroupSettings,\
    IDefaultLocalGroupPolicy
from collective.local.addgroup import api
from zope.component.hooks import getSite
from zope.lifecycleevent.interfaces import IObjectRemovedEvent


def create_groups_at_content_creation(obj, event):
    if getattr(obj, 'isTemporary', lambda: False)():
        return
    elif getattr(obj, '_at_creation_flag', False):
        return
    elif IObjectRemovedEvent.providedBy(event):
        return
    elif obj.REQUEST.get('_local_groups_setup', False):
        return

    assert len(api.getGroupIds(obj)) == 0

    obj.REQUEST['_local_groups_setup'] = True
    settings = getUtility(IRegistry).forInterface(IAddNewGroupSettings)
    if not settings.add_new_group_at_creation:
        return


    policy = IDefaultLocalGroupPolicy(obj)
    gtool = getToolByName(getSite(), 'portal_groups')
    for group_info in policy.get_group_infos():
        group_id = group_info['id']
        counter = 1
        while gtool.getGroupById(group_id):
            group_id = "%s-%s" % (group_info['id'], counter)

        gtool.addGroup(group_id,
                       properties=group_info['properties'])
        api.addGroup(group_id, obj)
        obj.manage_setLocalRoles(group_id,
                                 group_info['local_roles'])
