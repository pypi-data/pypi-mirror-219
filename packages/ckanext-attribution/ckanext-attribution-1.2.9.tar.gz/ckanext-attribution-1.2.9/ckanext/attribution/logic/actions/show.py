#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools

from ckanext.attribution.logic.actions.meta import help, schema
from ckanext.attribution.model.crud import (
    AgentAffiliationQuery,
    AgentContributionActivityQuery,
    AgentQuery,
    ContributionActivityQuery,
    PackageContributionActivityQuery,
    PackageQuery,
)
from ckantools.decorators import action
from fuzzywuzzy import fuzz
from sqlalchemy import or_

from ckan.plugins import toolkit


@action(schema.agent_affiliation_show, help.agent_affiliation_show, get=True)
def agent_affiliation_show(original_data_dict):
    item_id = original_data_dict.pop('id')
    return AgentAffiliationQuery.read(item_id).as_dict()


@action(schema.agent_show, help.agent_show, get=True)
def agent_show(original_data_dict):
    item_id = original_data_dict.pop('id')
    return AgentQuery.read(item_id).as_dict()


@action(schema.agent_list, help.agent_list, get=True)
def agent_list(q, mode='normal'):
    if q is not None and q != '':
        q_string = '{0}%'.format(q)
        name_cols = [
            AgentQuery.m.name,
            AgentQuery.m.family_name,
            AgentQuery.m.given_names,
        ]
        name_parts = [
            subq
            for c in name_cols
            for subq in [c.ilike('{0}%'.format(p)) for p in q.split(' ')]
        ]
        q_parts = [*name_parts, AgentQuery.m.external_id.ilike(q_string)]
        portal_results = AgentQuery.search(or_(*q_parts))
    else:
        portal_results = AgentQuery.all()
    results = [a.as_dict() for a in portal_results]
    if mode == 'duplicates':
        results = [
            r for r in results if fuzz.token_set_ratio(q, r['display_name']) >= 90
        ]
    return results


@action(
    schema.agent_contribution_activity_show,
    help.agent_contribution_activity_show,
    get=True,
)
def agent_contribution_activity_show(original_data_dict):
    item_id = original_data_dict.pop('id')
    return AgentContributionActivityQuery.read(item_id).as_dict()


@action(schema.contribution_activity_show, help.contribution_activity_show, get=True)
def contribution_activity_show(original_data_dict):
    item_id = original_data_dict.pop('id')
    return ContributionActivityQuery.read(item_id).as_dict()


@action(
    schema.package_contribution_activity_show,
    help.package_contribution_activity_show,
    get=True,
)
def package_contribution_activity_show(original_data_dict):
    item_id = original_data_dict.pop('id')
    return PackageContributionActivityQuery.read(item_id).as_dict()


@action(schema.package_contributions_show, help.package_contributions_show, get=True)
def package_contributions_show(context, original_data_dict, limit=None, offset=0):
    item_id = original_data_dict.pop('id')
    limit = int(limit) if limit is not None else None
    contributions = PackageQuery.get_contributions(item_id)
    by_agent = {
        k: list(v)
        for k, v in itertools.groupby(
            sorted(contributions, key=lambda x: x.agent.id), key=lambda x: x.agent.id
        )
    }
    total = len(by_agent)
    agent_order = [
        (
            {
                'agent': v[0].agent,
                'activities': [a.as_dict() for a in v],
                'affiliations': toolkit.get_action('agent_affiliations')(
                    context, {'agent_id': k, 'package_id': item_id}
                ),
            },
            v[0].agent.package_order(item_id),
        )
        for k, v in by_agent.items()
    ]
    sorted_contributions = [
        c
        for c, o in sorted(
            agent_order,
            key=lambda x: (x[1] if x[1] >= 0 else total, x[0]['agent'].sort_name),
        )
    ]

    page_end = offset + limit if limit is not None else total + 1
    contributions_dict = {
        'contributions': [
            {
                'agent': c['agent'].as_dict(),
                'activities': c['activities'],
                'affiliations': c['affiliations'],
            }
            for c in sorted_contributions[offset:page_end]
        ],
        'all_agents': [c['agent'].id for c in sorted_contributions],
        'total': total,
        'cited_total': len([x for x in agent_order if x[1] >= 0]),
        'offset': offset,
        'page_size': limit or total,
    }
    return contributions_dict


@action(schema.agent_affiliations, help.agent_affiliations, get=True)
def agent_affiliations(agent_id, package_id):
    agent = AgentQuery.read(agent_id)
    affiliations = agent.affiliations
    if package_id is not None:
        affiliations = [
            a
            for a in affiliations
            if a['affiliation'].package_id is None
            or a['affiliation'].package_id == package_id
        ]

    def _transform(a):
        detail = a.get('affiliation').as_dict()
        try:
            del detail['agent_a_id']
        except KeyError:
            pass
        try:
            del detail['agent_b_id']
        except KeyError:
            pass
        detail['other_agent'] = a.get('agent').as_dict()
        return detail

    return [_transform(a) for a in affiliations]
