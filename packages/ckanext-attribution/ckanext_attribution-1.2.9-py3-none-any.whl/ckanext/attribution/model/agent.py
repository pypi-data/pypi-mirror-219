#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import DomainObject, meta, user_table
from ckan.model.types import make_uuid
from ckan.plugins import toolkit
from sqlalchemy import Boolean, Column, ForeignKey, Table, UnicodeText

# this table stores agent
agent_table = Table(
    'agent',
    meta.metadata,
    Column('id', UnicodeText, primary_key=True, default=make_uuid),
    Column('agent_type', UnicodeText, nullable=False),
    Column('family_name', UnicodeText, nullable=True),
    Column('given_names', UnicodeText, nullable=True),
    Column('given_names_first', Boolean, nullable=True, default=True),
    Column('name', UnicodeText, nullable=True),
    Column('location', UnicodeText, nullable=True),
    Column('external_id', UnicodeText, nullable=True, unique=True),
    Column('external_id_scheme', UnicodeText, nullable=True),
    Column(
        'user_id',
        UnicodeText,
        ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=True,
    ),
)


class Agent(DomainObject):
    """
    An agent (e.g. a researcher or institution) that contributes to a package.
    """

    @property
    def display_name(self):
        if self.agent_type == 'person':
            return ' '.join(
                [self.given_names, self.family_name]
                if self.given_names_first
                else [self.family_name, self.given_names]
            )
        elif self.agent_type == 'org':
            name = self.name
            if self.location is not None:
                name += ' ({0})'.format(self.location)
            return name
        else:
            return self.name

    @property
    def standardised_name(self):
        """
        Family name first for persons.

        :return:
        """
        if self.agent_type == 'person':
            return ', '.join([self.family_name, self.given_names])
        else:
            return self.name

    @property
    def citation_name(self):
        return self.display_name if self.agent_type == 'person' else self.name

    @property
    def external_id_url(self):
        if self.external_id is None:
            return
        external_scheme_dict = toolkit.get_action('attribution_controlled_lists')(
            {}, {'lists': ['agent_external_id_schemes']}
        )['agent_external_id_schemes']
        return external_scheme_dict[self.external_id_scheme]['url'].format(
            self.external_id
        )

    @property
    def affiliations(self):
        return [
            {'agent': a.other_agent(self.id), 'affiliation': a}
            for a in self._affiliations
        ]

    def package_affiliations(self, pkg_id):
        return [
            a
            for a in self.affiliations
            if a['affiliation'].package_id is None
            or a['affiliation'].package_id == pkg_id
        ]

    def package_order(self, pkg_id):
        try:
            citation = next(
                c
                for c in self.contribution_activities
                if c.package
                and (c.package.id == pkg_id or c.package.name == pkg_id)
                and c.activity == '[citation]'
            )
        except StopIteration:
            return -1
        return citation.order

    @property
    def sort_name(self):
        return self.family_name if self.agent_type == 'person' else self.name

    def as_dict(self):
        agent_dict = super(Agent, self).as_dict()
        agent_dict['display_name'] = self.display_name
        agent_dict['standardised_name'] = self.standardised_name
        agent_dict['external_id_url'] = self.external_id_url
        return agent_dict


def check_for_table():
    """
    Checks to see if the user_table exists and creates it if it doesn't.
    """
    if user_table.exists():
        agent_table.create(checkfirst=True)
