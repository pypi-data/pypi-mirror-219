#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools
import re

from ckan.plugins import toolkit, plugin_loaded
from ckanext.attribution.model.crud import PackageQuery, AgentQuery


def can_edit():
    """
    Check editing permissions for updating agent directly.

    :return:
    """
    try:
        permitted = toolkit.check_access('agent_update', {}, {})
        return permitted
    except toolkit.NotAuthorized:
        return False


def split_caps(string_input):
    return re.sub('(.)(?=[A-Z][^A-Z])', '\\1 ', string_input)


def get_contributions(pkg_id):
    '''
    Template access for the
    :func:`~ckanext.attribution.model.crud.PackageQuery.get_contributions` query method.
    :param pkg_id:
    :return:
    '''
    return PackageQuery.get_contributions(pkg_id)


def get_cited_contributors(pkg_id):
    contributions = PackageQuery.get_contributions(pkg_id)
    by_agent = {
        k: list(v)
        for k, v in itertools.groupby(
            sorted(contributions, key=lambda x: x.agent.id), key=lambda x: x.agent.id
        )
    }

    def _citation_order(entry):
        activities = entry[1]
        citation = [a.order for a in activities if a.activity == '[citation]']
        if citation:
            return max(citation)
        else:
            return -1

    entries = [
        {
            'agent': c[1][0].agent,
            'contributions': [a for a in c[1] if a.activity != '[citation]'],
            'order': _citation_order(c),
        }
        for c in by_agent.items()
    ]

    cited_agents = {
        'cited' if k else 'uncited': sorted(list(v), key=lambda x: x['order'])
        for k, v in itertools.groupby(
            sorted(entries, key=lambda x: x['order']), key=lambda x: x['order'] != -1
        )
    }
    if 'cited' not in cited_agents:
        cited_agents['cited'] = []
    if 'uncited' not in cited_agents:
        cited_agents['uncited'] = []
    return cited_agents


def controlled_list(list_name):
    return toolkit.get_action('attribution_controlled_lists')(
        {}, {'lists': [list_name]}
    )[list_name]


def doi_plugin():
    return plugin_loaded('doi')


def agent_from_user(user_id):
    matches = AgentQuery.search(AgentQuery.m.user_id == user_id)
    if matches:
        return matches[0]
    else:
        return


def user_contributions(user_id):
    agent = agent_from_user(user_id)
    if not agent:
        return []
    pkg_show = toolkit.get_action('package_show')
    by_package = {
        k: list(v)
        for k, v in itertools.groupby(
            sorted(agent.contribution_activities, key=lambda x: x.package.id),
            key=lambda x: x.package.id,
        )
    }
    package_details = []
    for k, v in by_package.items():
        try:
            pkg = pkg_show({}, {'id': k})
        except toolkit.NotAuthorized:
            continue
        activities = [x for x in v if x.activity != '[citation]']
        try:
            citation = next(x.order for x in v if x.activity == '[citation]')
        except StopIteration:
            citation = None
        package_details.append(
            {'dataset': pkg, 'activities': activities, 'citation': citation}
        )
    return package_details
