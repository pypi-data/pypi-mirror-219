#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import orcid
import requests
from ckan.plugins import toolkit
from werkzeug.utils import cached_property


class OrcidApi(object):
    """
    
    """

    def __init__(self):
        self.key = toolkit.config.get('ckanext.attribution.orcid_key')
        self.secret = toolkit.config.get('ckanext.attribution.orcid_secret')
        self._debug = toolkit.config.get('ckanext.attribution.debug', 'True') == 'True'

    @cached_property
    def conn(self):
        """
        
        """
        if self.key is None or self.secret is None:
            raise Exception(toolkit._('ORCID API credentials not supplied.'))
        return orcid.PublicAPI(self.key, self.secret, sandbox=self._debug)

    @cached_property
    def read_token(self):
        """
        
        """
        if self.key is None or self.secret is None:
            raise Exception(toolkit._('ORCID API credentials not supplied.'))
        url = (
            'https://sandbox.orcid.org/oauth/token'
            if self._debug
            else 'https://orcid.org/oauth/token'
        )
        r = requests.post(
            url,
            data={
                'client_id': self.key,
                'client_secret': self.secret,
                'grant_type': 'client_credentials',
                'scope': '/read-public',
            },
            headers={'Accept': 'application/json'},
        )
        if r.ok:
            return r.json()['access_token']
        else:
            return None

    def search(self, orcid_q=None, q=None, family_name=None, given_names=None):
        '''

        :param orcid_q:  (Default value = None)
        :param q:  (Default value = None)

        '''
        query = []
        if orcid_q is not None and orcid_q != '':
            query.append('orcid:' + orcid_q)
        if q is not None and q != '':
            query.append('text:' + q)
        if family_name is not None and family_name != '':
            query.append('family-name:' + family_name)
        if given_names is not None and given_names != '':
            query.append('given-names:' + given_names)
        query = '+AND+'.join(query)
        search_response = self.conn.search(query, access_token=self.read_token, rows=10)
        records = []
        loaded_ids = []
        for r in search_response.get('result', []):
            _id = r.get(u'orcid-identifier', {}).get(u'path', None)
            if _id is not None and _id not in loaded_ids:
                try:
                    orcid_record = self.as_agent_record(self.read(_id))
                    records.append(orcid_record)
                    loaded_ids.append(_id)
                except AttributeError as e:
                    # probably a malformed orcid record
                    continue
        result = {'total': search_response.get('num-found', 0), 'records': records}
        return result

    def read(self, orcid_id):
        '''


        :param orcid_id:

        '''
        record = self.conn.read_record_public(orcid_id, 'record', self.read_token)
        return record

    def as_agent_record(self, orcid_record):
        '''


        :param orcid_record:

        '''
        names = orcid_record.get('person', {}).get('name', {})
        return {
            'family_name': names.get('family-name', {}).get('value', ''),
            'given_names': names.get('given-names', {}).get('value', ''),
            'external_id': orcid_record.get('orcid-identifier', {}).get('path', ''),
            'external_id_scheme': 'orcid',
            'agent_type': 'person',  # default
        }
