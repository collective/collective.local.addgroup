from zope.configuration import xmlconfig
from plone.app.testing import (
    PloneSandboxLayer, applyProfile, IntegrationTesting,
    FunctionalTesting, login, logout, layers)

PLONE_FIXTURE = layers.PloneFixture()


class AddGroupLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.local.addgroup
        xmlconfig.file('configure.zcml', collective.local.addgroup, context=configurationContext)


MY_PRODUCT_FIXTURE = AddGroupLayer()
MY_PRODUCT_INTEGRATION_TESTING = IntegrationTesting(bases=(MY_PRODUCT_FIXTURE,), name="AddGroupLayer:Integration")
