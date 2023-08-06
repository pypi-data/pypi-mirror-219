#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK
import re

from ckan.plugins import toolkit
from ckanext.attribution.lib.orcid_api import OrcidApi
from ckanext.attribution.lib.ror_api import RorApi
from ckanext.attribution.model.crud import AgentQuery
from ckantools.decorators import action
from ckanext.attribution.logic.actions.meta import schema, help


@action(
    schema.attribution_controlled_lists, help.attribution_controlled_lists, get=True
)
def attribution_controlled_lists(context, lists=None):
    all_lists = {
        'agent_types': {
            'person': {'fa_icon': 'fas fa-user', 'default_scheme': 'orcid'},
            'org': {'fa_icon': 'fas fa-building', 'default_scheme': 'ror'},
            'other': {'fa_icon': 'fas fa-asterisk', 'default_scheme': None},
        },
        'contribution_activity_types': {
            'credit': [
                {'name': 'Conceptualization'},
                {'name': 'Data curation'},
                {'name': 'Formal analysis'},
                {'name': 'Funding acquisition'},
                {'name': 'Investigation'},
                {'name': 'Methodology'},
                {'name': 'Project administration'},
                {'name': 'Resources'},
                {'name': 'Software'},
                {'name': 'Supervision'},
                {'name': 'Validation'},
                {'name': 'Visualization'},
                {'name': 'Writing – original draft'},
                {'name': 'Writing – review & editing'},
            ],
            'datacite': [
                {'name': 'ContactPerson'},
                {'name': 'DataCollector'},
                {'name': 'DataCurator'},
                {'name': 'DataManager'},
                {'name': 'Distributor'},
                {'name': 'Editor'},
                {'name': 'HostingInstitution'},
                {'name': 'Other'},
                {'name': 'Producer'},
                {'name': 'ProjectLeader'},
                {'name': 'ProjectManager'},
                {'name': 'ProjectMember'},
                {'name': 'RegistrationAgency'},
                {'name': 'RegistrationAuthority'},
                {'name': 'RelatedPerson'},
                {'name': 'ResearchGroup'},
                {'name': 'RightsHolder'},
                {'name': 'Researcher'},
                {'name': 'Sponsor'},
                {'name': 'Supervisor'},
                {'name': 'WorkPackageLeader'},
            ],
            'internal': [{'name': 'Unspecified'}],
        },
        'contribution_activity_levels': ['Lead', 'Supporting', 'Equal'],
        'agent_external_id_schemes': {
            'orcid': {
                'url': 'https://orcid.org/{0}',
                'scheme_uri': 'https://orcid.org',
                'label': 'ORCID',
                'fa_icon': 'fab fa-orcid',
                'rgx': r'(?:\d{4}-){3}\d{3}[\dX]',
            },
            'ror': {
                'url': 'https://ror.org/{0}',
                'scheme_uri': 'https://ror.org',
                'label': 'ROR',
                'fa_icon': 'fas fa-university',
                'rgx': r'0[0-9a-hjkmnp-z]{6}\d{2}',
            },
        },
    }
    if lists is not None and isinstance(lists, str):
        lists = [l.strip() for l in lists.split(',')]
    if lists is not None and isinstance(lists, list):
        lists = [l for l in lists if l in all_lists]
        return {k: v for k, v in all_lists.items() if k in lists}
    else:
        return all_lists


@action(schema.agent_external_search, help.agent_external_search, get=True)
def agent_external_search(q, sources):
    if sources is not None and isinstance(sources, str):
        sources = [sources.lower()]
    elif sources is not None and isinstance(sources, list):
        sources = [s.lower() for s in sources]
    elif sources is not None:
        sources = None
    results = {}
    if q is None or q == '':
        return results

    # ORCID
    if sources is None or 'orcid' in sources:
        orcid_remaining = 0
        orcidapi = OrcidApi()
        orcid_search = orcidapi.search(q=q)
        n = orcid_search.get(u'total', 0)
        orcid_records = orcid_search.get('records')
        orcid_records = [
            r
            for r in orcid_records
            if AgentQuery.read_external_id(r['external_id']) is None
        ]
        if n > len(orcid_records):
            orcid_remaining = n - len(orcid_records)
        results['orcid'] = {'records': orcid_records, 'remaining': orcid_remaining}

    # ROR
    if sources is None or 'ror' in sources:
        ror_remaining = 0
        rorapi = RorApi()
        ror_search = rorapi.search(q=q)
        n = ror_search.get(u'total', 0)
        ror_records = ror_search.get('records')
        ror_records = [
            r
            for r in ror_records
            if AgentQuery.read_external_id(r['external_id']) is None
        ]
        if n > len(ror_records):
            ror_remaining = n - len(ror_records)
        results['ror'] = {'records': ror_records, 'remaining': ror_remaining}

    return results


@action(schema.agent_external_read, help.agent_external_read, get=True)
def agent_external_read(agent_id, external_id, external_id_scheme, diff=False):
    if agent_id is None and (external_id is None or external_id_scheme is None):
        raise toolkit.Invalid(
            'Either record ID or external ID + scheme must be provided.'
        )
    if agent_id is not None:
        updated_dict = AgentQuery.read_from_external_api(agent_id)
        updated_dict['id'] = agent_id
        del updated_dict[
            'user_id'
        ]  # this is internal only so it's always going to be None
        if diff:
            item_dict = AgentQuery.read(agent_id).as_dict()
            for k, v in item_dict.items():
                if k in updated_dict and updated_dict.get(k) == v:
                    del updated_dict[k]
        return updated_dict
    else:
        apis = {'orcid': OrcidApi, 'ror': RorApi}
        api = apis[external_id_scheme.lower()]()
        return api.as_agent_record(api.read(external_id))


@action(schema.validate_external_id, help.validate_external_id)
def validate_external_id(context, external_id, external_id_scheme):
    # extract via regex first
    controlled_lists = toolkit.get_action('attribution_controlled_lists')(context, {})
    scheme = controlled_lists['agent_external_id_schemes'][external_id_scheme.lower()]
    rgx = re.compile(scheme['rgx'])
    matches = rgx.findall(external_id)
    if not matches:
        return {'id': None, 'error': 'No valid ID string found.'}
    api = {'orcid': OrcidApi, 'ror': RorApi}[external_id_scheme.lower()]()
    for match in matches:
        try:
            record = api.read(match)
            if record:
                return {'id': match, 'error': None}
        except Exception as e:
            continue
    return {'id': None, 'error': '{0} ID could not be found'.format(external_id_scheme)}
