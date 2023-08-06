# encoding: utf-8

"""Tests for notifications.py."""

from ckan import model
from ckan.plugins import toolkit
import ckan.tests.factories as factories
from ckan.tests.helpers import reset_db

import os


class TestExtraNotificationRecipients(object):

    @classmethod
    def setup(self):
        reset_db()
        ini_path = os.path.dirname(os.path.abspath(__file__)) + "../../../../test.ini"
        os.system("ckan -c " + ini_path + " harvester initdb")

    def test_get_extra_email_notification(self):
        context, source_id = self._create_harvest_source_with_owner_org_and_job_if_not_existing()

        new_rec_action = toolkit.get_action("harvest_get_notifications_recipients")
        new_recipients = new_rec_action(context, {'source_id': source_id})

        assert {'email': u'john@gmail.com', 'name': u'john@gmail.com'} in new_recipients
        assert {'email': u'peter@gmail.com', 'name': u'peter@gmail.com'} in new_recipients

    def _create_harvest_source_with_owner_org_and_job_if_not_existing(self):
        site_user = toolkit.get_action('get_site_user')(
            {'model': model, 'ignore_auth': True}, {})['name']

        context = {
            'user': site_user,
            'model': model,
            'session': model.Session,
            'ignore_auth': True,
        }

        test_org = factories.Organization(extras=[{'key': 'email_list', 'value': 'john@gmail.com, peter@gmail.com'}])
        # test_other_org = factories.Organization()
        org_admin_user = factories.User()
        org_member_user = factories.User()

        toolkit.get_action('organization_member_create')(
            context.copy(),
            {
                'id': test_org['id'],
                'username': org_admin_user['name'],
                'role': 'admin'
            }
        )

        toolkit.get_action('organization_member_create')(
            context.copy(),
            {
                'id': test_org['id'],
                'username': org_member_user['name'],
                'role': 'member'
            }
        )

        source_dict = {
            'title': 'Test Source 01',
            'name': 'test-source-01',
            'url': 'basic_test',
            'source_type': 'ckan',
            'owner_org': test_org['id'],
            'run': True
        }

        harvest_source = toolkit.get_action('harvest_source_create')(
            context.copy(),
            source_dict
        )

        return context, harvest_source['id']

    def test_create_harvest_source_with_no_org(self):
        context, source_id = self._create_harvest_source_with_no_org()

        new_rec_action = toolkit.get_action("harvest_get_notifications_recipients")
        new_recipients = new_rec_action(context, {'source_id': source_id})

        assert new_recipients == []

    def _create_harvest_source_with_no_org(self):
        site_user = toolkit.get_action('get_site_user')(
            {'model': model, 'ignore_auth': True}, {})['name']

        context = {
            'user': site_user,
            'model': model,
            'session': model.Session,
            'ignore_auth': True,
        }

        source_dict = {
            'title': 'Test Source 02',
            'name': 'test-source-02',
            'url': 'basic_test2',
            'source_type': 'ckan',
            'run': True
        }

        harvest_source = toolkit.get_action('harvest_source_create')(
            context.copy(),
            source_dict
        )

        return context, harvest_source['id']
