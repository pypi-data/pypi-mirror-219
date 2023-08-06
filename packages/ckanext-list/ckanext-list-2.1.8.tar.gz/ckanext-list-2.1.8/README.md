<!--header-start-->
<img src="https://data.nhm.ac.uk/images/nhm_logo.svg" align="left" width="150px" height="100px" hspace="40"/>

# ckanext-list

[![Tests](https://img.shields.io/github/actions/workflow/status/NaturalHistoryMuseum/ckanext-list/main.yml?style=flat-square)](https://github.com/NaturalHistoryMuseum/ckanext-list/actions/workflows/main.yml)
[![Coveralls](https://img.shields.io/coveralls/github/NaturalHistoryMuseum/ckanext-list/main?style=flat-square)](https://coveralls.io/github/NaturalHistoryMuseum/ckanext-list)
[![CKAN](https://img.shields.io/badge/ckan-2.9.7-orange.svg?style=flat-square)](https://github.com/ckan/ckan)
[![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg?style=flat-square)](https://www.python.org/)
[![Docs](https://img.shields.io/readthedocs/ckanext-list?style=flat-square)](https://ckanext-list.readthedocs.io)

_A CKAN extension that adds a list view for resources._

<!--header-end-->

# Overview

<!--overview-start-->
This extension adds a list view for resources on a CKAN instance. Records are listed as brief summaries, with a configurable set of fields shown for each.

**NB**: This extension currently only works with the Natural History Museum's theme extension [ckanext-nhm](https://github.com/NaturalHistoryMuseum/ckanext-nhm); this [should be fixed](https://github.com/NaturalHistoryMuseum/ckanext-list/issues/9) in future releases (contributions are always welcome).

<!--overview-end-->

# Installation

<!--installation-start-->
Path variables used below:
- `$INSTALL_FOLDER` (i.e. where CKAN is installed), e.g. `/usr/lib/ckan/default`
- `$CONFIG_FILE`, e.g. `/etc/ckan/default/development.ini`

## Installing from PyPI

```shell
pip install ckanext-list
```

## Installing from source

1. Clone the repository into the `src` folder:
   ```shell
   cd $INSTALL_FOLDER/src
   git clone https://github.com/NaturalHistoryMuseum/ckanext-list.git
   ```

2. Activate the virtual env:
   ```shell
   . $INSTALL_FOLDER/bin/activate
   ```

3. Install via pip:
   ```shell
   pip install $INSTALL_FOLDER/src/ckanext-list
   ```

### Installing in editable mode

Installing from a `pyproject.toml` in editable mode (i.e. `pip install -e`) requires `setuptools>=64`; however, CKAN 2.9 requires `setuptools==44.1.0`. See [our CKAN fork](https://github.com/NaturalHistoryMuseum/ckan) for a version of v2.9 that uses an updated setuptools if this functionality is something you need.

## Post-install setup

1. Add 'list' to the list of plugins in your `$CONFIG_FILE`:
   ```ini
   ckan.plugins = ... list
   ```

2. Install `lessc` globally:
   ```shell
   npm install -g "less@~4.1"
   ```

<!--installation-end-->

# Configuration

<!--configuration-start-->
There are currently no options that can be specified in your .ini config file.

<!--configuration-end-->

# Usage

<!--usage-start-->
To use the view in a template:

```html+jinja
<div data-module="list"
     data-module-resource = "{{ h.dump_json(resource_json) }}"
     data-module-resource-view = "{{ h.dump_json(resource_view_json) }}">
</div>

{% resource 'ckanext-list/main' %}
```

<!--usage-end-->

# Testing

<!--testing-start-->
There is a Docker compose configuration available in this repository to make it easier to run tests. The ckan image uses the Dockerfile in the `docker/` folder.

To run the tests against ckan 2.9.x on Python3:

1. Build the required images:
   ```shell
   docker-compose build
   ```

2. Then run the tests.
   The root of the repository is mounted into the ckan container as a volume by the Docker compose
   configuration, so you should only need to rebuild the ckan image if you change the extension's
   dependencies.
   ```shell
   docker-compose run ckan
   ```

<!--testing-end-->
