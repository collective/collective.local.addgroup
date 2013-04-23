# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel

from collective.local.addgroup import _
from ..interfaces import IAddNewGroupSettings

class AddNewGroupSettingsControlPanelEditForm(controlpanel.RegistryEditForm):

    schema = IAddNewGroupSettings
    label = _(u"Local group management settings")


class AddNewGroupSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = AddNewGroupSettingsControlPanelEditForm

