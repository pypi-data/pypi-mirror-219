# encoding: utf-8

'''Tests for the ckanext.datagovcatalog extension.'''

import ckan.plugins


class TestDatagovCatalogPluginLoaded(object):
    '''Tests for the ckanext.datagovcatalog.plugin module.'''

    def test_plugin_loaded(self):
        assert ckan.plugins.plugin_loaded('datagovcatalog')
