from zope.i18n import translate
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from AccessControl.SecurityManagement import getSecurityManager

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from plone.app.controlpanel.usergroups import GroupDetailsControlPanel

from plone.app.layout.viewlets.common import ViewletBase
from collective.local.addgroup import api, PMF, _


class RemoveGroupFromList(BrowserView):
    def __call__(self):
        form = self.request.form
        if 'groupname' in form:
            groupname = form['groupname']
            api.removeGroup(groupname, self.context)
        target_url = self.context.absolute_url() + "/@@sharing"
        self.request.response.redirect(target_url)


class AddGroupToListJS(ViewletBase):

    def render(self):
        return u"""
<script type="text/javascript">
  jQuery(document).ready(function(){
    if (jQuery('#new-group-link')) {
        jQuery('#user-group-sharing-settings input[name=entries.type:records][value=group]').each(function() {
            value = jQuery(this).siblings('input[name=entries.id:records]').attr('value');
            if (value != 'AuthenticatedUsers') {
                if (jQuery("#groups-list a[href$='groupname="+value+"']").length == 0) {
                    html = '<a href="@@add-group-to-list?groupname='+value+'"><img src="'+portal_url+'/++resource++addgroup.gif" title="%s" /></a>'
                    img = jQuery(this).siblings('img');
                    jQuery(html).insertAfter(img);
                    img.remove();
                }
            }
        });
    }
  });
</script>
""" % translate(_(u"Add to managed groups"), context=self.request)


class AddGroupToList(BrowserView):
    def __call__(self):
        form = self.request.form
        if 'groupname' in form:
            groupname = form['groupname']
            gtool = getToolByName(self.context, 'portal_groups')
            g = gtool.getGroupById(groupname)
            if g is not None:
                api.addGroup(groupname, self.context)

        target_url = self.context.absolute_url() + "/@@sharing"
        self.request.response.redirect(target_url)



class AddGroupInSharing(ViewletBase):

    def update(self):
        gtool = getToolByName(self.context, 'portal_groups')
        groups = api.getGroupIds(self.context)
        self.groups = []
        for gid in groups:
            g = gtool.getGroupById(gid)
            if g is not None:
                self.groups.append(g)

        self.groups.sort(key=lambda g: normalizeString(g.getProperty('title'),
                                                       context=self.context))
        sm = getSecurityManager()
        self.can_add_groups = sm.checkPermission(
                'Add Groups', self.context)
        self.can_manage_groups = sm.checkPermission(
                'Manage users', self.context)
        self.delete_confirmation_msg = translate(
                _(u"Are you sure you want to delete?"),
                context=self.request)

    def content(self):
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
                    context=self.request),
                )


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
            api.addGroup(groupname, self.context)

            roles = self.request.form.get('localroles', [])
            if roles:
                self.context.manage_setLocalRoles(groupname, roles)
                self.context.reindexObjectSecurity()

        return result

    def roles(self):
        vocabulary = getUtility(IVocabularyFactory, 'LocalRoles')
        return vocabulary(self.context)
