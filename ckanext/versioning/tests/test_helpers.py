import mock
from ckan.tests import factories
from nose.tools import assert_equals

from ckanext.versioning.logic import helpers
from ckanext.versioning.tests import (FunctionalTestBase, mocked_action,
                                      mocked_backend)


@mock.patch(mocked_action, return_value=mocked_backend)
class TestHelpers(FunctionalTestBase):

    def setup(self):
        super(TestHelpers, self).setup()

        self.admin_user = factories.Sysadmin()

        self.org = factories.Organization(
            users=[
                {'name': self.admin_user['name'], 'capacity': 'admin'},
            ]
        )
        with mock.patch(mocked_action, return_value=mocked_backend):
            self.dataset = factories.Dataset(owner_org=self.org['id'],
                                             private=False)

    def test_dataset_has_link_resources(self, mocked_backend):
        upload_resource = factories.Resource(
            package_id=self.dataset['id'],
            url_type='upload'
        )
        link_resource = factories.Resource(
            package_id=self.dataset['id'],
            url_type=''
        )

        self.dataset['resources'].extend([upload_resource, link_resource])

        assert_equals(
            helpers.has_link_resources(self.dataset),
            True)

    def test_dataset_does_not_has_link_resources(self, mocked_backend):
        upload_resource = factories.Resource(
            package_id=self.dataset['id'],
            url_type='upload'
        )

        self.dataset['resources'].append(upload_resource)

        assert_equals(
            helpers.has_link_resources(self.dataset),
            False)