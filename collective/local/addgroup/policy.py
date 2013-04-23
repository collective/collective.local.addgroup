from zope.interface import implements
from zope.i18n import translate

from collective.local.addgroup.interfaces import IDefaultLocalGroupPolicy
from collective.local.addgroup import _, api


class DefaultLocalGroupPolicy(object):
    implements(IDefaultLocalGroupPolicy)

    def __init__(self, context):
        self.context = context

    def get_group_infos(self):
        return [{'id': "%s-members" % self.context.getId(),
                 'properties': {'title': translate(_("${folder} members",
                                        mapping={'folder': self.context.Title()}),
                                        context=self.context.REQUEST)},
                 'local_roles': ('Reader', 'Contributor', 'Editor'),
                 },
                ]

    def get_default_group_id(self):
        return api.getGroupIds(self.context)[0]