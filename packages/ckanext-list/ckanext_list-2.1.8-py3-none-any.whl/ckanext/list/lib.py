# !/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-list
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit


def get_datastore_fields(resource_id, context):
    """
    Returns a list of alphabetically sorted field names for the given resource id from
    the datastore.

    :param resource_id: the resource's ID
    :param context: the context to use when calling the datastore_search action
    :return: list of field names
    """
    data = {'resource_id': resource_id, 'limit': 0}
    fields = toolkit.get_action('datastore_search')(context, data).get('fields', {})
    return sorted([f['id'] for f in fields])
