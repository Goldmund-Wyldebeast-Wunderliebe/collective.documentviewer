from collective.documentviewer.settings import GlobalSettings
from zope.event import notify
from Products.Archetypes.event import ObjectInitializedEvent
# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry import Registry
from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.documentviewer.testing import DocumentViewer_INTEGRATION_TESTING
from collective.documentviewer.testing import createObject
from collective.documentviewer.convert import Converter
from collective.documentviewer.settings import Settings

import os

_files = os.path.join(os.path.dirname(__file__), 'test_files')


class RegistryTest(unittest.TestCase):

    layer = DocumentViewer_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_converts(self):
        fi = createObject(self.portal, 'File', 'test1',
            file=open(os.path.join(_files, 'test.pdf')))
        settings = Settings(fi)
        self.assertEqual(settings.successfully_converted, None)
        notify(ObjectInitializedEvent(fi))
        self.assertEqual(settings.successfully_converted, True)
        self.assertEqual(settings.num_pages, 1)

    def test_auto_assigns_view(self):
        fi = createObject(self.portal, 'File', 'test1',
            file=open(os.path.join(_files, 'test.pdf')))
        gsettings = GlobalSettings(self.portal)
        gsettings.auto_select_layout = True
        notify(ObjectInitializedEvent(fi))
        self.assertEqual(fi.getLayout(), 'documentviewer')

    def test_not_auto_assigns_view(self):
        fi = createObject(self.portal, 'File', 'test1',
            file=open(os.path.join(_files, 'test.pdf')))
        gsettings = GlobalSettings(self.portal)
        gsettings.auto_select_layout = False
        notify(ObjectInitializedEvent(fi))
        self.assertTrue(fi.getLayout() != 'documentviewer')

    def test_auto_convert_word(self):
        fi = createObject(self.portal, 'File', 'test1',
            file=open(os.path.join(_files, 'test.doc')))
        gsettings = GlobalSettings(self.portal)
        gsettings.auto_select_layout = True
        gsettings.auto_layout_file_types = ['word']
        notify(ObjectInitializedEvent(fi))
        settings = Settings(fi)
        self.assertEqual(settings.successfully_converted, True)
        self.assertEqual(settings.num_pages, 2)

    def test_auto_convert_powerpoint(self):
        fi = createObject(self.portal, 'File', 'test1',
            file=open(os.path.join(_files, 'test.odp')))
        gsettings = GlobalSettings(self.portal)
        gsettings.auto_select_layout = True
        gsettings.auto_layout_file_types = ['ppt']
        notify(ObjectInitializedEvent(fi))
        settings = Settings(fi)
        self.assertEqual(settings.successfully_converted, True)
        self.assertEqual(settings.num_pages, 1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
