import ckan.tests.factories as factories
from ckan.tests import helpers
from ckanext.datagovcatalog.helpers.packages import update_tracking_info_to_package


class TestOverridePackage(object):

    def test_override_package(self):

        pkg_dict = {
            'name': 'dataset1',
            'organization': {
                'name': 'org1',
                'organization_type': 'Federal Government'
            },
            'resources': [
                {'url': 'http://resources.com/resouce1.json'},
                {'url': 'http://resources.com/resouce2.csv'},
                {'url': 'http://resources.com/resouce3.html'}
            ]
        }

        new_pkg_dict = {
            'name': 'dataset1',
            'organization': {
                'name': 'org1'
            },
            'tracking_summary': 'some tracking info',
            'resources': [
                {'url': 'http://resources.com/resouce1.json', 'tracking_summary': 'tracking info 1'},
                {'url': 'http://resources.com/resouce2.csv', 'tracking_summary': 'tracking info 2'},
                {'url': 'http://resources.com/resouce3.html', 'tracking_summary': 'tracking info 3'}
            ]
        }

        final_pkg = update_tracking_info_to_package(pkg_dict, new_pkg_dict)

        assert final_pkg['tracking_summary'] == 'some tracking info'
        assert final_pkg['organization']['organization_type'] == 'Federal Government'

        asserts = 0
        for resource in final_pkg['resources']:
            if resource['url'] == 'http://resources.com/resouce1.json':
                assert resource['tracking_summary'] == 'tracking info 1'
                asserts += 1
            elif resource['url'] == 'http://resources.com/resouce2.csv':
                assert resource['tracking_summary'] == 'tracking info 2'
                asserts += 1
            elif resource['url'] == 'http://resources.com/resouce3.html':
                assert resource['tracking_summary'] == 'tracking info 3'
                asserts += 1

        assert asserts == 3

    @helpers.change_config('ckanext.datagovcatalog.add_packages_tracking_info', 'false')
    def test_disable_tracking(self):
        org = factories.Organization()
        dataset = factories.Dataset(owner_org=org['id'])
        context = {'ignore_auth': True}
        dataset_show = helpers.call_action(
            "package_show",
            context=context,
            id=dataset['name']
        )

        assert 'tracking_summary' not in dataset_show
