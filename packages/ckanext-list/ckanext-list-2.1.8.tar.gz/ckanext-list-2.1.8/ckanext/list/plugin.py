#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-list
# Created by the Natural History Museum in London, UK

import json
from logging import getLogger

from ckan.plugins import SingletonPlugin, implements, interfaces, toolkit
from ckanext.list.lib import get_datastore_fields
from ckanext.list.logic.validators import is_datastore_field

log = getLogger(__name__)
ignore_empty = toolkit.get_validator('ignore_empty')


class ListPlugin(SingletonPlugin):
    """
    Summary dataset view.

    Provides a summary view of records, to replace the grid.
    """

    implements(interfaces.IConfigurer, inherit=True)
    implements(interfaces.IResourceView, inherit=True)

    ## IConfigurer
    def update_config(self, config):
        """
        Add our template directories to the list of available templates.

        :param config:
        """
        toolkit.add_template_directory(config, 'theme/templates')
        toolkit.add_public_directory(config, 'theme/public')
        toolkit.add_resource('theme/assets', 'ckanext-list')

    def view_template(self, context, data_dict):
        return 'list/list_view.html'

    def form_template(self, context, data_dict):
        return 'list/list_form.html'

    def can_view(self, data_dict):
        """
        Specify which resources can be viewed by this plugin.

        :param data_dict: return: boolean
        :returns: boolean
        """
        # Check that we have a datastore for this resource
        if data_dict['resource'].get('datastore_active', False):
            return True
        return False

    ## IResourceView
    def info(self):
        return {
            'name': 'list',
            'title': 'List',
            'schema': {
                'title_field': [is_datastore_field],
                'secondary_title_field': [ignore_empty, is_datastore_field],
                'fields': [ignore_empty, is_datastore_field],
                'image_field': [ignore_empty, is_datastore_field],
                'image_delimiter': [ignore_empty],
            },
            'icon': 'list-alt',
            'iframed': True,
            'filterable': True,
            'preview_enabled': True,
            'full_page_edit': False,
        }

    def setup_template_variables(self, context, data_dict):
        """
        Setup variables available to templates.

        :param context:
        :param data_dict:
        """
        datastore_fields = get_datastore_fields(data_dict['resource']['id'], context)
        return {
            'resource_json': json.dumps(data_dict['resource']),
            'resource_view_json': json.dumps(data_dict['resource_view']),
            # Fields - used in the form display options
            'fields': [{'text': f, 'value': f} for f in datastore_fields],
        }
