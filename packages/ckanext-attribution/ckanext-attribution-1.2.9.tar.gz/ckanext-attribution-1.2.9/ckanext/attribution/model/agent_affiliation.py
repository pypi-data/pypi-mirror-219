#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import DomainObject, meta
from ckan.model.types import make_uuid
from ckanext.attribution.model.agent import agent_table
from sqlalchemy import Column, Date, ForeignKey, Table, UnicodeText

agent_affiliation_table = Table(
    'agent_affiliation',
    meta.metadata,
    Column('id', UnicodeText, primary_key=True, default=make_uuid),
    Column(
        'agent_a_id',
        UnicodeText,
        ForeignKey('agent.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    ),
    Column(
        'agent_b_id',
        UnicodeText,
        ForeignKey('agent.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    ),
    Column('affiliation_type', UnicodeText, nullable=True),
    Column('description', UnicodeText, nullable=True),
    Column('start_date', Date, nullable=True),
    Column('end_date', Date, nullable=True),
    Column(
        'package_id',
        UnicodeText,
        ForeignKey('package.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
    ),
)


class AgentAffiliation(DomainObject):
    """
    An affiliation between two agents (e.g. agent a is a researcher, agent b is a
    university).
    """

    @property
    def agents(self):
        return [self._agent_a, self._agent_b]

    def other_agent(self, agent_id):
        assert agent_id in [self.agent_a_id, self.agent_b_id]
        return self._agent_a if agent_id == self.agent_b_id else self._agent_b


def check_for_table():
    """
    
    """
    if agent_table.exists():
        agent_affiliation_table.create(checkfirst=True)
