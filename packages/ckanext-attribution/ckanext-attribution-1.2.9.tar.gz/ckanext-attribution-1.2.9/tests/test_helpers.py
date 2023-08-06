import pytest
from ckan.tests import factories
from ckan.common import g
from ckanext.attribution.lib import helpers


@pytest.mark.filterwarnings('ignore::sqlalchemy.exc.SADeprecationWarning')
@pytest.mark.ckan_config('ckan.plugins', 'attribution')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
def test_can_edit_non_superuser():
    user = factories.User()
    g.user = user['name']
    assert not helpers.can_edit()


@pytest.mark.filterwarnings('ignore::sqlalchemy.exc.SADeprecationWarning')
@pytest.mark.ckan_config('ckan.plugins', 'attribution')
@pytest.mark.usefixtures('clean_db', 'with_plugins', 'with_request_context')
def test_can_edit_superuser():
    user = factories.Sysadmin()
    g.user = user['name']
    assert helpers.can_edit()
