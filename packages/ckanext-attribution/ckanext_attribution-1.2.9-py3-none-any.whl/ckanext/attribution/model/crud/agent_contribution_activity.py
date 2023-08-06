#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckanext.attribution.model.agent_contribution_activity import (
    AgentContributionActivity,
    agent_contribution_activity_table,
)

from ._base import BaseQuery


class AgentContributionActivityQuery(BaseQuery):
    """
    
    """

    # model and table (subclasses should override)
    m = AgentContributionActivity
    t = agent_contribution_activity_table

    @classmethod
    def read_agent_package(cls, agent_id, package_id):
        return [
            r.contribution_activity
            for r in cls.search(cls.m.agent_id == agent_id)
            if r.contribution_activity.package.id == package_id
        ]
