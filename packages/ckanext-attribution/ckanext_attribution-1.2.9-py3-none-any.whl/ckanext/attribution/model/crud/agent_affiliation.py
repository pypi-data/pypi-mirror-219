#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckanext.attribution.model.agent_affiliation import (
    AgentAffiliation,
    agent_affiliation_table,
)

from ._base import BaseQuery
from sqlalchemy import or_, and_


class AgentAffiliationQuery(BaseQuery):
    """
    
    """

    # model and table (subclasses should override)
    m = AgentAffiliation
    t = agent_affiliation_table

    @classmethod
    def read_agent(cls, agent_id, package_id=None):
        filters = [or_(cls.m.agent_a_id == agent_id, cls.m.agent_b_id == agent_id)]
        if package_id is not None:
            filters.append(cls.m.package_id == package_id)
        return cls.search(and_(*filters))
