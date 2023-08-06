<!--header-start-->
<img src="https://data.nhm.ac.uk/images/nhm_logo.svg" align="left" width="150px" height="100px" hspace="40"/>

# ckanext-attribution

[![Tests](https://img.shields.io/github/actions/workflow/status/NaturalHistoryMuseum/ckanext-attribution/main.yml?style=flat-square)](https://github.com/NaturalHistoryMuseum/ckanext-attribution/actions/workflows/main.yml)
[![Coveralls](https://img.shields.io/coveralls/github/NaturalHistoryMuseum/ckanext-attribution/main?style=flat-square)](https://coveralls.io/github/NaturalHistoryMuseum/ckanext-attribution)
[![CKAN](https://img.shields.io/badge/ckan-2.9.7-orange.svg?style=flat-square)](https://github.com/ckan/ckan)
[![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg?style=flat-square)](https://www.python.org/)
[![Docs](https://img.shields.io/readthedocs/ckanext-attribution?style=flat-square)](https://ckanext-attribution.readthedocs.io)

_A CKAN extension that adds support for complex attribution._

<!--header-end-->

# Overview

<!--overview-start-->
This extension standardises author/contributor attribution for datasets, enabling enhanced metadata
and greater linkage between datasets. It currently integrates with the [ORCID](https://orcid.org)
and [ROR](https://ror.org) APIs; contributors ('agents') can be added directly from these databases,
or manually.

Contributors can be added and edited via actions or via a Vue app that can be inserted into
the `package_metadata_fields.html` template snippet.

![A screenshot of the form for adding contributors when editing a package. At the top is a preview of the citation in APA format, then there are three example agents with their affiliations and contribution activities.](.github/screenshots/form-overview.png)

## Schema

The schema is (partially) based on
the [RDA/TDWG recommendations](https://github.com/tdwg/attribution). Three new models are
added: `Agent` (contributors), `ContributionActivity`, and `Affiliation` (plus small linking models
between these and `Package` records).

### `Agent`

Defines _one_ agent.

| Field               | Type   | Values                   | Notes                                                                                                                                                          |
|---------------------|--------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `agent_type`        | string | 'person', 'org', 'other' |                                                                                                                                                                |
| `family_name`       | string |                          | only used for 'person' records                                                                                                                                 |
| `given_names`       | string |                          | only used for 'person' records                                                                                                                                 |
| `given_names_first` | bool   | True, False              | only used for 'person' records; if the given names should be displayed first according to the person's culture/language (default True)                         |
| `name`              | string |                          | used for non-'person' records                                                                                                                                  |
| `location`          | string |                          | used for non-person records, optional; a location to display for the organisation to help differentiate between similar names (e.g. 'Natural History Museum (_ |

London_)' and 'Natural History Museum (_Dublin_)')
`external_id`|string||an identifier from an external service like ORCID or ROR
`external_id_scheme`|string|'orcid', 'ror', other|the scheme for the `external_id`; currently only 'orcid' and 'ror' are fully supported, though basic support for others can be implemented by adding to the `attribution_controlled_lists` [action](ckanext/attribution/logic/actions/extra.py#L14)
`user_id`|string|`User.id` foreign key|link to a user account on the CKAN instance

### `ContributionActivity`

Defines _one_ activity performed by _one_ agent on _one_ specific dataset.

| Field      | Type     | Values                        | Notes                                                                                                                                                                                                                                                                                                                                  |
|------------|----------|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `activity` | string   | [controlled vocabulary]       | the activity/role the agent is associated with, e.g. 'Editor', 'Methodology'; roles are defined in the `attribution_controlled_lists` [action](ckanext/attribution/logic/actions/extra.py#L14), which currently lists the [Datacite](https://datacite.org) and [CRediT](https://credit.niso.org) role taxonomies (but can be expanded) |
| `scheme`   | string   | [controlled vocabulary]       | name of the defined scheme from [`attribution_controlled_lists`](ckanext/attribution/logic/actions/extra.py#L14)                                                                                                                                                                                                                       |
| `level`    | string   | 'Lead', 'Equal', 'Supporting' | optional degree of contribution (from [CRediT](http://credit.niso.org/implementing-credit))                                                                                                                                                                                                                                            |
| `time`     | datetime |                               | optional date/time of the activity                                                                                                                                                                                                                                                                                                     |
| `order`    | integer  |                               | order of the agent within all who are associated with the same activity, e.g. 1st Editor, 3rd DataCollector (optional)                                                                                                                                                                                                                 |

A specialised `ContributionActivity` entry with a '[citation]' activity is used to define the order
in which contributors should be cited (and/or if they should be cited at all).

### `Affiliation`

Defines a relationship between _two_ agents, either as a 'universal' (persistent) affiliation or for
a single package (e.g. a project affiliation).

| Field              | Type   | Values                   | Notes                                                                              |
|--------------------|--------|--------------------------|------------------------------------------------------------------------------------|
| `agent_a_id`       | string | `Agent.id` foreign key   | one of the two agents (a/b order does not matter)                                  |
| `agent_b_id`       | string | `Agent.id` foreign key   | one of the two agents (a/b order does not matter)                                  |
| `affiliation_type` | string |                          | very short description (1 or 2 words) of affiliation, e.g. 'employment' (optional) |
| `description`      | string |                          | longer description of affiliation (optional)                                       |
| `start_date`       | date   |                          | date at which the relationship began, e.g. employment start date (optional)        |
| `end_date`         | date   |                          | date at which the relationship ended (optional)                                    |
| `package_id`       | string | `Package.id` foreign key | links affiliation to a specific package/dataset (optional)                         |

<!--overview-end-->

# Installation

<!--installation-start-->
Path variables used below:
- `$INSTALL_FOLDER` (i.e. where CKAN is installed), e.g. `/usr/lib/ckan/default`
- `$CONFIG_FILE`, e.g. `/etc/ckan/default/development.ini`

## Installing from PyPI

```shell
pip install ckanext-attribution
```

## Installing from source

1. Clone the repository into the `src` folder:
   ```shell
   cd $INSTALL_FOLDER/src
   git clone https://github.com/NaturalHistoryMuseum/ckanext-attribution.git
   ```

2. Activate the virtual env:
   ```shell
   . $INSTALL_FOLDER/bin/activate
   ```

3. Install via pip:
   ```shell
   pip install $INSTALL_FOLDER/src/ckanext-attribution
   ```

### Installing in editable mode

Installing from a `pyproject.toml` in editable mode (i.e. `pip install -e`) requires `setuptools>=64`; however, CKAN 2.9 requires `setuptools==44.1.0`. See [our CKAN fork](https://github.com/NaturalHistoryMuseum/ckan) for a version of v2.9 that uses an updated setuptools if this functionality is something you need.

## Post-install setup

1. Add 'attribution' to the list of plugins in your `$CONFIG_FILE`:
   ```ini
   ckan.plugins = ... attribution
   ```

2. Install `lessc` globally:
   ```shell
   npm install -g "less@~4.1"
   ```

3. Add this block to `package_metadata_fields.html` to show the Vue app:
   ```jinja2
   {% block package_custom_fields_agent %}
        {{ super() }}
   {% endblock %}
   ```

4. Change the `authors` field in your SOLR `schema.xml` to set up faceting.
   ```xml
   <schema>
       <fields>
           <...>
           <field name="author" type="string" indexed="true" stored="true" multiValued="true"/>
           <...>
       </fields>
       <...>
       <copyField source="author" dest="text"/>
   </schema>
   ```

   After making the changes, restart SOLR and reindex (`ckan -c $CONFIG_FILE search-index rebuild`).
   You will also have to enable the config option (see below) to see this in the UI.

<!--installation-end-->

# Configuration

<!--configuration-start-->
These are the options that can be specified in your .ini config file. NB:
setting `ckanext.attribution.debug` to `True` means that the API
accesses [sandbox.orcid.org](https://sandbox.orcid.org) instead of [orcid.org](https://orcid.org).
Although both run by the ORCID organisation, these are _different websites_ and you will need a
separate account/set of credentials for each. It is also worth noting that you will not have access
to the full set of authors on the sandbox.

## API credentials [REQUIRED]

| Name                               | Description                  | Options |
|------------------------------------|------------------------------|---------|
| `ckanext.attribution.orcid_key`    | Your ORCID API client ID/key |         |
| `ckanext.attribution.orcid_secret` | Your ORCID API client secret |         |

## Optional

| Name                                  | Description                                                           | Options    | Default |
|---------------------------------------|-----------------------------------------------------------------------|------------|---------|
| `ckanext.attribution.debug`           | If true, use sandbox.orcid.org (for testing)                          | True/False | True    |
| `ckanext.attribution.enable_faceting` | Enable filtering by contributor name (requires change to SOLR schema) | True/False | False   |

<!--configuration-end-->

# Usage

<!--usage-start-->
## Actions

This extension adds numerous new actions. These are primarily CRUD actions for managing models, with
inline documentation and predictable interactions. It's probably more helpful to only go over the
more "unusual" new actions here.

### `agent_list`

Search for agents by name or external ID, or just list all agents.

```python
data_dict = {
    'q': 'QUERY',  # optional; searches in name, family_name, given_names, and external_id
}

toolkit.get_action('agent_list')({}, data_dict)
```

### `package_contributions_show`

Show all contribution records for a package, grouped by agent. Optionally provide a limit and offset
for pagination.

```python
data_dict = {
    'id': 'PACKAGE_ID',
    'limit': 'PAGE_SIZE',
    'offset': 'OFFSET'
}

toolkit.get_action('package_contributions_show')({}, data_dict)
```

Returns a dict:

```python
{
    'contributions': [
        {
            'agent': {
                # Agent.as_dict()
            },
            'activities': [
                # list of Activity.as_dict()
            ],
            'affiliations': [
                {
                    'affiliation': {
                        # Affiliation.as_dict()
                    },
                    'other_agent': {
                        # Agent.as_dict()
                    }
                },
                # ...
            ]
        },
        # ...
    ],
    'total': total,
    'offset': offset,
    'page_size': limit or total
}
```

### `agent_affiliations`

Show all affiliations for a given agent, optionally limited to a specific dataset/package (plus '
global' affiliations).

```python
data_dict = {
    'agent_id': 'AGENT_ID',
    'package_id': 'PACKAGE_ID'  # optional
}

toolkit.get_action('agent_affiliations')({}, data_dict)
```

Returns a list of records formatted as such:

```python
{
    'affiliation': {
        # Affiliation.as_dict()
    },
    'other_agent': {
        # Agent.as_dict()
    }
}
```

### `attribution_controlled_lists`

Returns collections of defined values (which can be modified by using `@toolkit.chained_action`).

```python
data_dict = {
    'lists': ['NAME1', 'NAME2']  # optional; only return these lists
}

toolkit.get_action('attribution_controlled_lists')({}, data_dict)
```

There are four collections:

1. `agent_types` describes valid types for agents and adds additional detail;
2. `contribution_activity_types` contains role/activity taxonomies (i.e. Datacite and CRediT) and
   lists the available activity values;
3. `contribution_activity_levels` is a list of contribution levels (i.e. 'lead', 'equal', and '
   supporting', from CRediT);
4. `agent_external_id_schemes` describes valid schemes for external IDs (currently, ORCID and ROR).

These collections are useful for validation and frontend connectivity/standardisation. They are
contained within an action to _a._ enable frontend access via AJAX requests, and _b._ allow users to
override values as needed.

### `agent_external_search`

Search external sources (ORCID and ROR) for agent data. Ignores records that already exist in the
database.

```python
data_dict = {
    'q': 'QUERY_STRING',
    'sources': ['SOURCE1', 'SOURCE2']  # optional; only search these sources
}

toolkit.get_action('agent_external_search')({}, data_dict)
```

Results are returned formatted as such:

```python
{
    'SCHEME_NAME': {
        'records': [
            # list of agent dicts
        ]
        'remaining': 10000  # number of other records found
    }
}
```

### `agent_external_read`

Read data from an external source like ORCID or ROR, either from an existing record or a new
external ID.

```python
# EITHER
data_dict_existing = {
    'agent_id': 'AGENT_ID',
    'diff': False
    # optional; only show values that differ from the record's current values (default False)
}

# OR
data_dict_new = {
    'external_id': 'EXTERNAL_ID',
    'external_id_scheme': 'orcid'  # or 'ror', etc.
}

toolkit.get_action('agent_external_read')({}, data_dict)
```

## Commands

### `initdb`
```shell
ckan -c $CONFIG_FILE attribution initdb
```
Initialise database tables.

### `sync`
```shell
ckan -c $CONFIG_FILE attribution sync $OPTIONAL_ID $ANOTHER_OPTIONAL_ID
```
Retrieve up-to-date information from external APIs for contributors with an external ID set.

### `refresh-packages`
```shell
ckan -c $CONFIG_FILE attribution refresh-packages $OPTIONAL_ID $ANOTHER_OPTIONAL_ID
```
Update the author string for all (or the specified) packages.

### `agent-external-search`
```shell
ckan -c $CONFIG_FILE attribution agent-external-search --limit 10 $OPTIONAL_ID $ANOTHER_OPTIONAL_ID
```
Search external APIs for contributors without an external ID set. Run `refresh-packages` and rebuild the search index after this command.

### `merge-agents`
```shell
ckan -c $CONFIG_FILE attribution merge-agents --q $SEARCH_QUERY --match-threshold 75
```
Find agents with similar names (optionally matching the search query) and merge them. Run `refresh-packages` and rebuild the search index after this command.

### `migratedb`
```shell
ckan -c $CONFIG_FILE attribution migratedb --limit 10 --dry-run --no-search-api
```
Attempt to extract names of contributors from author fields and convert them to the new format.
- `--limit` will only convert a certain number of packages at a time.
- `--dry-run` prevents saving to the database.
- `--no-search-api` just extracts the names, without searching external APIs for contributors after.

It is recommended to run `merge-agents`, `refresh-packages`, and rebuild the search index after running this command.

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
