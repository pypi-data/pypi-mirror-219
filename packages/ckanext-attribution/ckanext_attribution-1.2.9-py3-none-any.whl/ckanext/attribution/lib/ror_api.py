#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import requests
import json


class RorApi(object):
    url = 'https://api.ror.org'

    def read(self, ror_id):
        '''


        :param ror_id:

        '''
        response = requests.get('{0}/organizations/{1}'.format(self.url, ror_id))
        if not response.ok:
            return None
        try:
            record = response.json()
        except json.JSONDecodeError:
            return None
        if record.get('id') is None:
            return None
        return record

    def search(self, q):
        response = requests.get(
            '{0}/organizations'.format(self.url), params={'query': q}
        )
        if not response.ok:
            search_response = {}
        else:
            try:
                search_response = response.json()
            except json.JSONDecodeError:
                search_response = {}
        return {
            'total': search_response.get('number_of_results', 0),
            'records': [
                self.as_agent_record(r) for r in search_response.get('items', [])
            ],
        }

    def as_agent_record(self, ror_record):
        '''


        :param ror_record:

        '''
        if ror_record is None:
            return {}
        address = ror_record.get('addresses')
        if address is not None and len(address) > 0:
            location = address[0].get('city')
        else:
            location = ror_record.get('country', {}).get('country_name')
        return {
            'name': ror_record.get('name', ''),
            'external_id': ror_record.get('id', '').split('/')[-1],
            'external_id_scheme': 'ror',
            'location': location,
            'agent_type': 'org',  # default
        }
