from zope.interface import Interface
from zope import schema
from zope.component.interfaces import IObjectEvent

from collective.local.addgroup import _

class IAddNewGroup(Interface):
    """Include a add new group link to the sharing tab.
    """


class IGroupRemoved(IObjectEvent):
    """Event notified when a group is removed from the list.
    """

    groupid = schema.TextLine(title=u"Group id")


class IAddNewGroupSettings(Interface):
    """Global configuration settings for local add group features
    """

    add_new_group_at_creation = schema.Bool(
        title=_("Each time a content with local group management is created, creates a group and links it to this new content"))


class IDefaultLocalGroupPolicy(Interface):
    """Policy to customize default group(s) creation policy
    """

    def get_group_infos(self):
        """Return a dictionary with:
            id: group id,
            properties: group properties (title, etc.),
            local_roles: group local roles
        """