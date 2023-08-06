#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckantools.validators import list_of_strings

from ckan.plugins import toolkit

# grab all the validator functions upfront
ignore_missing = toolkit.get_validator('ignore_missing')
not_missing = toolkit.get_validator('not_missing')
boolean_validator = toolkit.get_validator('boolean_validator')
isodate_validator = toolkit.get_validator('isodate')
int_validator = toolkit.get_validator('int_validator')

# CREATE ===========================================================================================

agent_affiliation_create = {
    'agent_a_id': [not_missing, str],
    'agent_b_id': [not_missing, str],
    'affiliation_type': [ignore_missing, str],
    'description': [ignore_missing, str],
    'start_date': [ignore_missing, isodate_validator],
    'end_date': [ignore_missing, isodate_validator],
}

agent_create = {
    'agent_type': [not_missing, str],
    'family_name': [ignore_missing, str],
    'given_names': [ignore_missing, str],
    'given_names_first': [ignore_missing, boolean_validator],
    'user_id': [ignore_missing, str],
    'name': [ignore_missing, str],
}

contribution_activity_create = {
    'package_id': [not_missing, str],
    'agent_id': [not_missing, str],
    'activity': [not_missing, str],
    'scheme': [not_missing, str],
    'level': [ignore_missing, str],
    'time': [ignore_missing, isodate_validator],
}

# DELETE ===========================================================================================

agent_affiliation_delete = {'id': [not_missing, str]}

agent_delete = {'id': [not_missing, str]}

agent_contribution_activity_delete = {'id': [not_missing, str]}

contribution_activity_delete = {
    'id': [not_missing, str],
}

package_contribution_activity_delete = {'id': [not_missing, str]}

# EXTRA ============================================================================================

attribution_controlled_lists = {'lists': [ignore_missing, list_of_strings()]}

agent_external_search = {
    'q': [not_missing, str],
    'sources': [ignore_missing, list_of_strings()],
}

agent_external_read = {
    'agent_id': [ignore_missing, str],
    'external_id': [ignore_missing, str],
    'external_id_scheme': [ignore_missing, str],
    'diff': [ignore_missing, boolean_validator],
}

validate_external_id = {
    'external_id': [not_missing, str],
    'external_id_scheme': [not_missing, str],
}

# SHOW =============================================================================================

agent_affiliation_show = {'id': [not_missing, str]}

agent_show = {'id': [not_missing, str]}

agent_list = {'q': [ignore_missing, str], 'mode': [ignore_missing, str]}

agent_contribution_activity_show = {'id': [not_missing, str]}

contribution_activity_show = {'id': [not_missing, str]}

package_contribution_activity_show = {'id': [not_missing, str]}

package_contributions_show = {
    'id': [not_missing, str],
    'limit': [ignore_missing, int_validator],
    'offset': [ignore_missing, int_validator],
}

agent_affiliations = {
    'agent_id': [not_missing, str],
    'package_id': [ignore_missing, str],
}

# UPDATE ===========================================================================================

agent_affiliation_update = {
    'id': [not_missing, str],
    'agent_a_id': [ignore_missing, str],
    'agent_b_id': [ignore_missing, str],
    'affiliation_type': [ignore_missing, str],
    'description': [ignore_missing, str],
    'start_date': [ignore_missing, isodate_validator],
    'end_date': [ignore_missing, isodate_validator],
}

agent_update = {
    'id': [not_missing, str],
    'agent_type': [ignore_missing, str],
    'family_name': [ignore_missing, str],
    'given_names': [ignore_missing, str],
    'given_names_first': [ignore_missing, boolean_validator],
    'user_id': [ignore_missing, str],
    'name': [ignore_missing, str],
}

agent_external_update = {'id': [not_missing, str]}

contribution_activity_update = {
    'id': [not_missing, str],
    'activity': [ignore_missing, str],
    'scheme': [ignore_missing, str],
    'level': [ignore_missing, str],
    'time': [ignore_missing, isodate_validator],
}
