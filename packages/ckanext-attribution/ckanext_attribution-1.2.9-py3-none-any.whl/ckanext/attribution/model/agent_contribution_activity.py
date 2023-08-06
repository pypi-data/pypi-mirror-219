#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import DomainObject, meta
from ckan.model.types import make_uuid
from ckanext.attribution.model.agent import agent_table
from ckanext.attribution.model.contribution_activity import contribution_activity_table
from sqlalchemy import Column, ForeignKey, Table, UnicodeText

agent_contribution_activity_table = Table(
    'agent_contribution_activity',
    meta.metadata,
    Column('id', UnicodeText, primary_key=True, default=make_uuid),
    Column(
        'agent_id',
        UnicodeText,
        ForeignKey('agent.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    ),
    Column(
        'contribution_activity_id',
        UnicodeText,
        ForeignKey('contribution_activity.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        unique=True,
    ),
)


class AgentContributionActivity(DomainObject):
    """
    A link between an agent and the contribution activity performed.
    """

    pass


def check_for_table():
    """
    
    """
    if agent_table.exists() and contribution_activity_table.exists():
        agent_contribution_activity_table.create(checkfirst=True)
