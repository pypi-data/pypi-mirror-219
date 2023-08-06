# !/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-list
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.list.lib import get_datastore_fields


def is_datastore_field(value, context):
    """
    Ensure field name exists in the resource datastore.

    :param value: field name
    :param context: return:
    :return: the field name if it is valid, otherwise raises toolkit.Invalid error
    :raises: toolkit.Invalid if the field name is invalid
    """
    existing_fields = get_datastore_fields(toolkit.c.resource['id'], context)
    if value:
        # there can just be one string or a list of strings
        fields = [value] if isinstance(value, str) else value
        # loop through values, making sure they're in the datastore
        if any(field not in existing_fields for field in fields):
            raise toolkit.Invalid(toolkit._('Field not found in datastore'))

    return value
