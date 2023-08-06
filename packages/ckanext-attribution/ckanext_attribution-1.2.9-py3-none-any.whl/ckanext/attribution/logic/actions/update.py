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
    AgentQuery,
    ContributionActivityQuery,
    AgentAffiliationQuery,
    AgentContributionActivityQuery,
)
from ckantools.decorators import action, basic_action
from ckanext.attribution.logic.actions.meta import help, schema


@action(schema.agent_affiliation_update, help.agent_affiliation_update)
def agent_affiliation_update(context, original_data_dict, agent_a_id, agent_b_id):
    item_id = original_data_dict.pop('id')
    # check agents exist if updating
    for agent_id in [agent_a_id, agent_b_id]:
        if agent_id is None:
            continue
        try:
            toolkit.get_action('agent_show')(context, {'id': agent_id})
        except toolkit.ObjectNotFound:
            raise toolkit.ValidationError(
                'Agent ({0}) does not exist.'.format(agent_id)
            )
    affiliation = AgentAffiliationQuery.update(item_id, **original_data_dict)
    if affiliation is None:
        raise toolkit.ValidationError(
            'Unable to update affiliation. Check the fields are valid.'
        )
    return affiliation.as_dict()


@action(schema.agent_update, help.agent_update)
def agent_update(original_data_dict, agent_type=None):
    item_id = original_data_dict.get('id')
    current_record = AgentQuery.read(item_id)
    old_citation_name = current_record.citation_name
    if agent_type is None:
        agent_type = current_record.agent_type
    original_data_dict['agent_type'] = agent_type
    data_dict = AgentQuery.validate(original_data_dict)
    new_agent = AgentQuery.update(item_id, **original_data_dict)
    if new_agent.citation_name != old_citation_name:
        # if the name has been updated, the author strings need to be updated everywhere else too
        agent_id_column = AgentContributionActivityQuery.m.agent_id
        contrib_activities = AgentContributionActivityQuery.search(
            agent_id_column == item_id
        )
        packages = list(
            set([c.contribution_activity.package.id for c in contrib_activities])
        )
        for p in packages:
            author_string = get_author_string(package_id=p)
            toolkit.get_action('package_revise')(
                {}, {'match': {'id': p}, 'update': {'author': author_string}}
            )
    if new_agent is None:
        raise toolkit.ValidationError(
            'Unable to update agent. Check the fields are valid.'
        )
    return new_agent.as_dict()


@action(schema.agent_external_update, help.agent_external_update)
def agent_external_update(original_data_dict):
    item_id = original_data_dict.pop('id')
    updated_dict = AgentQuery.read_from_external_api(item_id)
    updated_agent = AgentQuery.update(item_id, **updated_dict)
    if updated_agent is None:
        raise toolkit.ValidationError(
            'Unable to update agent. Check the fields are valid.'
        )
    return updated_agent.as_dict()


@action(schema.contribution_activity_update, help.contribution_activity_update)
def contribution_activity_update(original_data_dict):
    item_id = original_data_dict.get('id')
    data_dict = ContributionActivityQuery.validate(original_data_dict)
    new_activity = ContributionActivityQuery.update(item_id, **data_dict)
    return new_activity.as_dict()


@toolkit.chained_action
@basic_action
def package_update(next_func, context, data_dict):
    parse_contributors(context, data_dict)
    data_dict['author'] = get_author_string(package_id=data_dict['id'])
    return next_func(context, data_dict)
