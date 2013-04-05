from zope.component.interfaces import ObjectEvent
from zope.interface import implements

from collective.local.addgroup.interfaces import IGroupRemoved


class GroupRemoved(ObjectEvent):
    implements(IGroupRemoved)

    def __init__(self, obj, groupid):
        self.object = obj
        self.groupid = groupid
