#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.model import Session
from ckan.plugins import toolkit
from ckanext.attribution.lib.orcid_api import OrcidApi
from ckanext.attribution.lib.ror_api import RorApi
from ckanext.attribution.model.agent import Agent, agent_table
from requests import HTTPError

from ._base import BaseQuery


class AgentQuery(BaseQuery):
    """
    CRUD methods for :class:`~ckanext.attribution.model.agent.Agent`.

    Fields
    ======
    :param agent_type: broad type of agent; usually 'person' or 'org'
    :type agent_type: str
    :param external_id: the agent's ID from an external service like ORCID or ROR
    :type external_id: str, optional
    :param external_id_scheme: the name of the scheme for the external ID, e.g. 'orcid' or 'ror'
    :type external_id_scheme: str, optional
    :param family_name: family name of an person [person only, required]
    :type family_name: str, optional
    :param given_names: given name(s) or initials of an person [person only, required]
    :type given_names: str, optional
    :param given_names_first: whether given names should be displayed before the family name
                              (default True) [person only, optional]
    :type given_names_first: bool, optional
    :param user_id: the ID for a registered user of this CKAN instance associated with this agent
                    [person only, optional]
    :type user_id: str, optional
    :param name: name of an organisation [org only, required]
    :type name: str, optional
    """

    #: :type: The associated database model type.
    m = Agent

    #: :sqlalchemy.Table: The associated database table instance (agent_table).
    t = agent_table

    @classmethod
    def validate(cls, data_dict):
        data_dict = super(AgentQuery, cls).validate(data_dict)
        valid_agent_types = ['person', 'org', 'other']
        agent_type = toolkit.get_or_bust(data_dict, 'agent_type')
        if agent_type not in valid_agent_types:
            raise toolkit.Invalid(
                'Agent type must be one of {0}'.format(', '.join(valid_agent_types))
            )

        valid_params = {
            'person': dict(
                required=['family_name', 'given_names'], optional=['given_names_first']
            ),
            'org': dict(required=['name'], optional=['location']),
            'other': dict(required=[], optional=[]),
        }
        required = ['agent_type'] + valid_params[agent_type]['required']
        optional = ['user_id', 'external_id', 'external_id_scheme'] + valid_params[
            agent_type
        ]['optional']
        for k in required:
            if k not in data_dict:
                raise toolkit.ValidationError('{0} is a required field.'.format(k))
        if 'external_id' in data_dict and 'external_id_scheme' not in data_dict:
            raise toolkit.ValidationError(
                'external_id_scheme is a required field when external_id is set.'
            )
        all_fields = required + optional
        for k in data_dict:
            if k not in all_fields:
                data_dict[k] = None
        return data_dict

    @classmethod
    def read_external_id(cls, eid):
        """
        Retrieve an agent record by its external identifier.

        :param eid: the full external ID (e.g. ORCID or ROR ID) of the record
        :type eid: str
        :returns: One agent or None if not found.
        :rtype: Agent
        """
        return Session.query(Agent).filter(Agent.external_id == eid).first()

    @classmethod
    def read_from_external_api(cls, agent_id, api=None):
        record = cls.read(agent_id)
        if record.external_id is None:
            raise Exception(toolkit._('Record does not have an external ID set.'))
        if record.external_id_scheme is None:
            raise Exception(toolkit._('External ID scheme not set.'))
        external_id_schemes = toolkit.get_action('attribution_controlled_lists')(
            {}, {'lists': ['agent_external_id_schemes']}
        )['agent_external_id_schemes']
        if record.external_id_scheme not in external_id_schemes:
            raise Exception(
                toolkit._(
                    'External ID scheme "{0}" not recognised.'.format(
                        record.external_id_scheme
                    )
                )
            )
        if record.external_id_scheme == 'orcid':
            return cls._read_from_orcid_api(record, api)
        elif record.external_id_scheme == 'ror':
            return cls._read_from_ror_api(record)
        else:
            raise NotImplementedError

    @classmethod
    def _read_from_orcid_api(cls, record, api=None):
        """
        Update the data for an agent using the ORCID API and the agent's stored ORCID.

        :param record: the existing record
        :type record: Agent
        :param api: an API instance already in use (useful if performing this action over many
                    agent records, to avoid instantiating many API connections) (Default value = None)
        :type api: OrcidApi
        :returns: the updated agent record
        :rtype: Agent
        """
        if api is None:
            api = OrcidApi()
        try:
            orcid_record = api.as_agent_record(api.read(record.external_id))
        except HTTPError:
            orcid_results = api.search(orcid_q=record.external_id)
            if orcid_results['total'] == 0:
                raise Exception(
                    toolkit._(
                        'This ORCID ({0}) does not exist.'.format(record.external_id)
                    )
                )
            else:
                orcid_record = orcid_results['records'][0]
        orcid_record['id'] = record.id
        return cls.validate(orcid_record)

    @classmethod
    def _read_from_ror_api(cls, record):
        """
        Update the data for an agent using the ROR API and the agent's stored ROR ID.

        :param record: the existing record
        :type record: Agent
        :returns: the updated agent record
        :rtype: Agent
        """
        api = RorApi()
        ror_record = api.read(record.external_id)
        if ror_record is None:
            raise Exception(
                toolkit._(
                    'Unable to find this ROR ID ({0}).'.format(record.external_id)
                )
            )
        updated_entry = api.as_agent_record(ror_record)
        updated_entry['id'] = record.id
        return cls.validate(updated_entry)
