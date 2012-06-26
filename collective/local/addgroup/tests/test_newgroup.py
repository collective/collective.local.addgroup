import unittest2 as unittest
from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName

from plone.testing.z2 import Browser
from plone.app.testing import login
from plone.app.testing.interfaces import (
    SITE_OWNER_NAME,
    TEST_USER_ID,
    TEST_USER_NAME,
    TEST_USER_PASSWORD)

from ..testing import MY_PRODUCT_INTEGRATION_TESTING


class CreateNewUserTests(unittest.TestCase):

    layer = MY_PRODUCT_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        portal.manage_permission("Manage users",
                roles=['Reviewer', 'Manager'], acquire=True)
        portal.manage_permission("Add Groups",
                roles=['Reviewer', 'Manager'], acquire=True)

#        mtool = getToolByName(portal, "portal_membership")
#        user = mtool.getMemberById(TEST_USER_ID)

    def create_folder(self):
        portal = self.layer['portal']
        app = aq_parent(portal)
        login(app, SITE_OWNER_NAME)
        portal.invokeFactory('Folder', 'test-folder',
            title="Test Folder")
        folder = portal['test-folder']
        folder.manage_setLocalRoles(TEST_USER_ID, ('Reviewer', ))
        folder.reindexObjectSecurity()
        return folder

    def test_create_new_group(self):
        app = self.layer['app']
        portal = self.layer['portal']
        folder = self.create_folder()
        import transaction
        transaction.commit()
        browser = Browser(app)
        browser.handleErrors = False
        # login
        portalURL = portal.absolute_url()
        browser.open(portalURL + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()

        browser.getLink(folder.Title()).click()
#        open('/tmp/testbrowser.html', 'w').write(browser.contents)

        browser.getLink('Sharing').click()
        browser.getLink('Add New Group').click()
        browser.getControl(name='addname').value = 'folder-members'
        browser.getControl(name='title:string').value = "Folder members"
        browser.getControl(name='localroles:list').value = ["Reader"]
        browser.getControl(name='form.button.Save').click()
        self.assertIn("Folder members (folder-members)", browser.contents)
