from AccessControl import getSecurityManager
from persistent.list import PersistentList

from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.event import notify
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.Five import BrowserView

from plone.app.controlpanel.usergroups import GroupDetailsControlPanel
from plone.app.layout.viewlets.common import ViewletBase

PMF = MessageFactory('plone')
_ = MessageFactory('addgroup')

ANNOTATION_KEY = 'collective.local.addgroup.groups'