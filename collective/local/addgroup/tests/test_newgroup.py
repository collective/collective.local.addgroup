import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import login
from plone.app.testing.interfaces import (
    SITE_OWNER_NAME,
    TEST_USER_ID,
    TEST_USER_NAME,
    TEST_USER_PASSWORD)

from ..testing import MY_PRODUCT_FUNCTIONAL_TESTING
from ..interfaces import IGroupRemoved


class CreateNewUserTests(unittest.TestCase):

    layer = MY_PRODUCT_FUNCTIONAL_TESTING

    def test_create_new_group(self):
        app = self.layer['app']
        portal = self.layer['portal']
        folder = portal['test-folder']
        self.browser = browser = Browser(app)
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
        self.assertIn("remove-folder-members", browser.contents)

    def test_remove_group(self):
        self.test_create_new_group()
        from zope.component import eventtesting
        eventtesting.setUp()
        browser = self.browser
        browser.getControl(name="remove-folder-members").click()
        self.assertNotIn("remove-folder-members", browser.contents)
        self.assertIn("Folder members", browser.contents)
        events = eventtesting.getEvents(IGroupRemoved)
        self.assertEqual(len(events), 1)
        eventtesting.clearEvents()
