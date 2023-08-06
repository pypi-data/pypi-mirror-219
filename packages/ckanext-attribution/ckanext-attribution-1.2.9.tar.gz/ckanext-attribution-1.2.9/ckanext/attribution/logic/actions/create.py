#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from ckanext.attribution.logic.actions.helpers import (
    parse_contributors,
    get_author_string,
)
from ckanext.attribution.model.crud import (
    AgentContributionActivityQuery,
    AgentQuery,
    ContributionActivityQuery,
    PackageContributionActivityQuery,
    AgentAffiliationQuery,
)
from ckantools.decorators import action, basic_action
from ckanext.attribution.logic.actions.meta import help, schema


@action(schema.agent_affiliation_create, help.agent_affiliation_create)
def agent_affiliation_create(context, original_data_dict, agent_a_id, agent_b_id):
    for agent_id in [agent_a_id, agent_b_id]:
        try:
            toolkit.get_action('agent_show')(context, {'id': agent_id})
        except toolkit.ObjectNotFound:
            raise toolkit.ValidationError(
                'Agent ({0}) does not exist.'.format(agent_id)
            )
    new_affiliation = AgentAffiliationQuery.create(**original_data_dict)
    if new_affiliation is None:
        raise toolkit.ValidationError(
            'Unable to create affiliation. Check the fields are valid.'
        )
    return new_affiliation.as_dict()


@action(schema.agent_create, help.agent_create)
def agent_create(original_data_dict):
    AgentQuery.validate(original_data_dict)
    new_agent = AgentQuery.create(**original_data_dict)
    if new_agent is None:
        raise toolkit.ValidationError(
            'Unable to create agent. Check the fields are valid.'
        )
    return new_agent.as_dict()


@action(schema.contribution_activity_create, help.contribution_activity_create)
def contribution_activity_create(context, original_data_dict, package_id, agent_id):
    try:
        toolkit.get_action('package_show')(context, {'id': package_id})
    except toolkit.ObjectNotFound:
        raise toolkit.ValidationError(
            'Cannot create activity for a package ({0}) that does not exist.'.format(
                package_id
            )
        )
    try:
        toolkit.get_action('agent_show')(context, {'id': agent_id})
    except toolkit.ObjectNotFound:
        raise toolkit.ValidationError(
            'Cannot create activity for an agent ({0}) that does not exist.'.format(
                agent_id
            )
        )
    new_activity = ContributionActivityQuery.create(**original_data_dict)
    PackageContributionActivityQuery.create(
        package_id=package_id, contribution_activity_id=new_activity.id
    )
    AgentContributionActivityQuery.create(
        agent_id=agent_id, contribution_activity_id=new_activity.id
    )
    return new_activity.as_dict()


@basic_action
@toolkit.chained_action
def package_create(next_func, context, data_dict):
    data_dict['author'] = 'pending'
    # we need the package ID to create links, but that's not created yet - so run the other
    # functions first
    created_pkg = next_func(context, data_dict)
    created_pkg['attribution'] = data_dict.get('attribution', '{}')
    parse_contributors(context, created_pkg)

    data_dict['author'] = get_author_string(package_id=created_pkg['id'])
    return data_dict
