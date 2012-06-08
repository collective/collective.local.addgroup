import pkg_resources
from AccessControl import getSecurityManager
from persistent.list import PersistentList

from zope.schema.interfaces import IVocabularyFactory
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString, safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.controlpanel.usergroups import GroupDetailsControlPanel
from plone.app.layout.viewlets.common import ViewletBase

PMF = MessageFactory('plone')
_ = MessageFactory('addgroup')

ANNOTATION_KEY = 'collective.local.addgroup.groups'


def addGroup(groupid, context):
    annotations = IAnnotations(context)
    groups = annotations.setdefault(ANNOTATION_KEY, PersistentList())
    if groupid not in groups:
        groups.append(groupid)


def getGroupIds(context):
    annotations = IAnnotations(context)
    groups = annotations.get(ANNOTATION_KEY, ())
    return tuple(groups)


class AddGroupInSharing(ViewletBase):

    def update(self):
        gtool = getToolByName(self.context, 'portal_groups')
        groups = getGroupIds(self.context)
        self.groups = []
        for gid in groups:
            g = gtool.getGroupById(gid)
            if g is not None:
                self.groups.append(g)

        self.groups.sort(key=lambda g: normalizeString(g.getProperty('title'),
                                                       context=self.context))

    def content(self):
        sm = getSecurityManager()
        if not sm.checkPermission('Add Groups', self.context):
            return u""

        return u"""
<script type="text/javascript">
  jQuery(document).ready(function(){
    jQuery('#new-group-link').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      formselector: 'form[name="groups"]',
      noform: function(el) {return jQuery.plonepopups.noformerrorshow(el, 'redirect');},
      redirect: function () {return location.href;}
    });
  });
</script>
<p><a href="%s" id="new-group-link">%s</a></p>""" % (
                '%s/@@add-new-group' % self.context.absolute_url(),
                translate(PMF(u"label_add_new_group", default=u"Add New Group"),
                    context=self.request))


class AddGroupForm(GroupDetailsControlPanel):

#    index = ViewPageTemplateFile(
#        pkg_resources.resource_filename('plone.app.controlpanel',
#            'usergroups_groupdetails.pt'))

    def __call__(self):
#        groupname = self.request.form.get('groupname', None)
#        if groupname is None:
#            addname = normalizeString(safe_unicode(self.context.Title()))
#            self.request.form['groupname'] = addname
#            self.request.form['title'] = self.context.Title()
        result = super(AddGroupForm, self).__call__()
        submitted = self.request.form.get('form.submitted', False)
        if submitted and self.group and not self.groupname:
            target_url = self.context.absolute_url() + "/@@sharing"
            self.request.response.redirect(target_url)
            groupname = self.group.getId()
            addGroup(groupname, self.context)

            roles = self.request.form.get('localroles', [])
            if roles:
                self.context.manage_setLocalRoles(groupname, roles)
                self.context.reindexObjectSecurity()

        return result

    def roles(self):
        vocabulary = getUtility(IVocabularyFactory, 'LocalRoles')
        return vocabulary(self.context)
