from zope.i18nmessageid import MessageFactory
from zope.i18n import translate
from plone.app.layout.viewlets.common import ViewletBase

from plone.app.controlpanel.usergroups import GroupDetailsControlPanel

PMF = MessageFactory('plone')
_ = MessageFactory('addgroup')


class AddGroupInSharing(ViewletBase):

    def update(self):
        pass

    def render(self):
        return u"""
<script type="text/javascript">
    jQuery(document).ready(function(){
        jQuery('#new-group-link').prepOverlay({subtype: 'ajax'});
    });
</script>
<p><a href="%s" id="new-group-link">%s</a></p>""" % (
                '%s/@@add-new-group' % self.context.absolute_url(),
                translate(PMF(u"heading_add_group_form", default=u"Add New Group"),
                    context=self.request))


class AddGroupForm(GroupDetailsControlPanel):

    def __call__(self):
        result = super(AddGroupForm, self).__call__()
        self.request.response.redirect(
                self.context.absolute_url() + "/@@sharing")
        return result
