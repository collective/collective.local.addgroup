from zope.annotation.interfaces import IAnnotations
from zope.event import notify
from persistent.list import PersistentList

from collective.local.addgroup import ANNOTATION_KEY
from collective.local.addgroup.event import GroupRemoved

def addGroup(groupid, context):
    annotations = IAnnotations(context)
    groups = annotations.setdefault(ANNOTATION_KEY, PersistentList())
    if groupid not in groups:
        groups.append(groupid)


def removeGroup(groupid, context):
    annotations = IAnnotations(context)
    groups = annotations.get(ANNOTATION_KEY, ())
    if groupid in groups:
        groups.remove(groupid)
        notify(GroupRemoved(context, groupid))


def getGroupIds(context):
    annotations = IAnnotations(context)
    groups = annotations.get(ANNOTATION_KEY, ())
    return tuple(groups)

