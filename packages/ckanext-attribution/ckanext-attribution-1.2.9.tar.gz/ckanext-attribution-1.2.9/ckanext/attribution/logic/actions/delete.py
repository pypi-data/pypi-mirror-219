#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckanext.attribution.logic.actions.meta import help, schema
from ckanext.attribution.model.crud import (
    AgentAffiliationQuery,
    AgentContributionActivityQuery,
    AgentQuery,
    ContributionActivityQuery,
    PackageContributionActivityQuery,
)
from ckantools.decorators import action


@action(schema.agent_affiliation_delete, help.agent_affiliation_delete)
def agent_affiliation_delete(original_data_dict):
    item_id = original_data_dict.pop('id')
    return AgentAffiliationQuery.delete(item_id)


@action(schema.agent_delete, help.agent_delete)
def agent_delete(original_data_dict):
    item_id = original_data_dict.pop('id')
    return AgentQuery.delete(item_id)


@action(
    schema.agent_contribution_activity_delete, help.agent_contribution_activity_delete
)
def agent_contribution_activity_delete(original_data_dict):
    item_id = original_data_dict.pop('id')
    return AgentContributionActivityQuery.delete(item_id)


@action(schema.contribution_activity_delete, help.contribution_activity_delete)
def contribution_activity_delete(original_data_dict):
    item_id = original_data_dict.pop('id')
    return ContributionActivityQuery.delete(item_id)


@action(
    schema.package_contribution_activity_delete,
    help.package_contribution_activity_delete,
)
def package_contribution_activity_delete(original_data_dict):
    item_id = original_data_dict.pop('id')
    return PackageContributionActivityQuery.delete(item_id)
