#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

"""
These relationships are defined separately to the object/table declarations to allow
them to reference each other without circular imports.
"""

from ckan.model import Package, User, meta
from sqlalchemy import or_
from sqlalchemy.orm import backref, relationship, attributes

from .agent import Agent, agent_table
from .agent_affiliation import AgentAffiliation, agent_affiliation_table
from .agent_contribution_activity import (
    AgentContributionActivity,
    agent_contribution_activity_table,
)
from .contribution_activity import ContributionActivity, contribution_activity_table
from .package_contribution_activity import (
    PackageContributionActivity,
    package_contribution_activity_table,
)


def setup_relationships():
    """
    Defines relationships/joins between the new models in ckanext-attribution.
    """

    # Agent
    manager = attributes.manager_of_class(Agent)
    if not manager or not manager.is_mapped:
        meta.mapper(
            Agent,
            agent_table,
            properties={
                'user': relationship(
                    User,
                    backref=backref('agent', cascade='all, delete-orphan'),
                    primaryjoin=agent_table.c.user_id.__eq__(User.id),
                ),
                'contribution_activities': relationship(
                    ContributionActivity, secondary=agent_contribution_activity_table
                ),
            },
        )

    # ContributionActivity
    manager = attributes.manager_of_class(ContributionActivity)
    if not manager or not manager.is_mapped:
        meta.mapper(
            ContributionActivity,
            contribution_activity_table,
            properties={
                'agent': relationship(
                    Agent, secondary=agent_contribution_activity_table, uselist=False
                ),
                'package': relationship(
                    Package,
                    secondary=package_contribution_activity_table,
                    uselist=False,
                ),
            },
        )

    # AgentAffiliation
    manager = attributes.manager_of_class(AgentAffiliation)
    if not manager or not manager.is_mapped:
        meta.mapper(
            AgentAffiliation,
            agent_affiliation_table,
            properties={
                '_agent_backref': relationship(
                    Agent,
                    backref=backref('_affiliations', cascade='all, delete-orphan'),
                    primaryjoin=or_(
                        agent_affiliation_table.c.agent_a_id.__eq__(Agent.id),
                        agent_affiliation_table.c.agent_b_id.__eq__(Agent.id),
                    ),
                ),
                '_agent_a': relationship(
                    Agent,
                    primaryjoin=agent_affiliation_table.c.agent_a_id.__eq__(Agent.id),
                ),
                '_agent_b': relationship(
                    Agent,
                    primaryjoin=agent_affiliation_table.c.agent_b_id.__eq__(Agent.id),
                ),
                'package': relationship(
                    Package,
                    primaryjoin=agent_affiliation_table.c.package_id == Package.id,
                ),
            },
        )

    # AgentContributionActivity
    manager = attributes.manager_of_class(AgentContributionActivity)
    if not manager or not manager.is_mapped:
        meta.mapper(
            AgentContributionActivity,
            agent_contribution_activity_table,
            properties={
                'agent': relationship(
                    Agent,
                    backref=backref(
                        'contribution_activity_link', cascade='all, delete-orphan'
                    ),
                    primaryjoin=agent_contribution_activity_table.c.agent_id.__eq__(
                        Agent.id
                    ),
                ),
                'contribution_activity': relationship(
                    ContributionActivity,
                    backref=backref('agent_link', cascade='all, delete-orphan'),
                    primaryjoin=agent_contribution_activity_table.c.contribution_activity_id.__eq__(
                        ContributionActivity.id
                    ),
                ),
            },
        )

    # PackageContributionActivity
    manager = attributes.manager_of_class(PackageContributionActivity)
    if not manager or not manager.is_mapped:
        meta.mapper(
            PackageContributionActivity,
            package_contribution_activity_table,
            properties={
                'package': relationship(
                    Package,
                    backref=backref(
                        'contribution_activity_link', cascade='all, delete-orphan'
                    ),
                    primaryjoin=package_contribution_activity_table.c.package_id.__eq__(
                        Package.id
                    ),
                ),
                'contribution_activity': relationship(
                    ContributionActivity,
                    backref=backref('package_link', cascade='all, delete-orphan'),
                    primaryjoin=package_contribution_activity_table.c.contribution_activity_id.__eq__(
                        ContributionActivity.id
                    ),
                ),
            },
        )
