from ckanext.list.plugin import ListPlugin


def test_can_view_yes():
    plugin = ListPlugin()
    assert plugin.can_view({'resource': {'datastore_active': True}})


def test_can_view_no1():
    plugin = ListPlugin()
    assert not plugin.can_view({'resource': {'datastore_active': False}})


def test_can_view_no2():
    plugin = ListPlugin()
    assert not plugin.can_view({'resource': {}})
