from ckan.tests import factories, helpers
from nose.tools import assert_equals

from . import FunctionalTestBase


class TestVersionsActions(FunctionalTestBase):
    """Test cases for logic actions
    """

    _load_plugins = ['versions']

    def setup(self):

        super(TestVersionsActions, self).setup()

        self.org_admin = factories.User()
        self.org_admin_name = self.org_admin['name'].encode('ascii')

        self.org_member = factories.User()
        self.org_member_name = self.org_member['name'].encode('ascii')

        self.org = factories.Organization(
            users=[
                {'name': self.org_member['name'], 'capacity': 'member'},
                {'name': self.org_admin['name'], 'capacity': 'admin'},
            ]
        )

        self.dataset = factories.Dataset()

    def test_list(self):
        versions = helpers.call_action('dataset_version_list',
                                       package_id=self.dataset['id'])
        assert_equals(len(versions), 1)

    def test_create(self):
        """Test basic dataset version creation
        """
        version = helpers.call_action(
            'dataset_version_create',
            dataset=self.dataset['id'],
            name="Version 0.1.2",
            description="The best dataset ever, it **rules!**")

        assert_equals(version['package_id'], self.dataset['id'])
        assert_equals(version['package_revision_id'],
                      self.dataset['revision_id'])
        assert_equals(version['description'],
                      "The best dataset ever, it **rules!**")
