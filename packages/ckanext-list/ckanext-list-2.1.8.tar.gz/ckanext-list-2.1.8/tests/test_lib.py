from unittest.mock import MagicMock, patch

from ckanext.list.lib import get_datastore_fields


def test_get_datastore_fields():
    result = {
        'fields': [
            {'id': 'beans'},
            {'id': 'lemons'},
            {'id': 'goats'},
        ]
    }
    mock_toolkit = MagicMock(
        get_action=MagicMock(return_value=MagicMock(return_value=result))
    )

    with patch('ckanext.list.lib.toolkit', mock_toolkit):
        assert get_datastore_fields(MagicMock(), MagicMock()) == [
            'beans',
            'goats',
            'lemons',
        ]


def test_get_datastore_fields_empty():
    result = {'fields': []}
    mock_toolkit = MagicMock(
        get_action=MagicMock(return_value=MagicMock(return_value=result))
    )

    with patch('ckanext.list.lib.toolkit', mock_toolkit):
        assert get_datastore_fields(MagicMock(), MagicMock()) == []


def test_get_datastore_fields_missing():
    result = {}
    mock_toolkit = MagicMock(
        get_action=MagicMock(return_value=MagicMock(return_value=result))
    )

    with patch('ckanext.list.lib.toolkit', mock_toolkit):
        assert get_datastore_fields(MagicMock(), MagicMock()) == []
