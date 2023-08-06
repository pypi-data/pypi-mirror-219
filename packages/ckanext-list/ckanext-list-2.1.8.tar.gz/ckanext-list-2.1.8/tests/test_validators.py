import pytest
from ckan.plugins import toolkit
from unittest.mock import patch, MagicMock

from ckanext.list.logic.validators import is_datastore_field


@pytest.mark.filterwarnings('ignore::sqlalchemy.exc.SADeprecationWarning')
@pytest.mark.usefixtures('with_request_context')
def test_is_datastore_field_valid():
    toolkit.c.resource = {'id': MagicMock()}
    fields = ['field1', 'field2']
    get_datastore_fields_mock = MagicMock(return_value=fields)
    with patch(
        'ckanext.list.logic.validators.get_datastore_fields', get_datastore_fields_mock
    ):
        assert is_datastore_field('field1', MagicMock()) == 'field1'
        assert is_datastore_field('field2', MagicMock()) == 'field2'


@pytest.mark.filterwarnings('ignore::sqlalchemy.exc.SADeprecationWarning')
@pytest.mark.usefixtures('with_request_context')
def test_is_datastore_field_invalid():
    toolkit.c.resource = {'id': MagicMock()}
    fields = ['field1', 'field2']
    get_datastore_fields_mock = MagicMock(return_value=fields)
    with patch(
        'ckanext.list.logic.validators.get_datastore_fields', get_datastore_fields_mock
    ):
        with pytest.raises(toolkit.Invalid, match='Field not found in datastore'):
            is_datastore_field('field3', MagicMock())


@pytest.mark.filterwarnings('ignore::sqlalchemy.exc.SADeprecationWarning')
@pytest.mark.usefixtures('with_request_context')
def test_is_datastore_field_valid_multiple():
    toolkit.c.resource = {'id': MagicMock()}
    fields = ['field1', 'field2']
    get_datastore_fields_mock = MagicMock(return_value=fields)
    with patch(
        'ckanext.list.logic.validators.get_datastore_fields', get_datastore_fields_mock
    ):
        # both valid
        assert is_datastore_field(fields, MagicMock()) == fields


@pytest.mark.filterwarnings('ignore::sqlalchemy.exc.SADeprecationWarning')
@pytest.mark.usefixtures('with_request_context')
def test_is_datastore_field_invalid_multiple():
    toolkit.c.resource = {'id': MagicMock()}
    fields = ['field1', 'field2']
    get_datastore_fields_mock = MagicMock(return_value=fields)
    with patch(
        'ckanext.list.logic.validators.get_datastore_fields', get_datastore_fields_mock
    ):
        with pytest.raises(toolkit.Invalid, match='Field not found in datastore'):
            # first one is valid, second one isn't
            assert is_datastore_field(['field2', 'field3'], MagicMock()) == fields
