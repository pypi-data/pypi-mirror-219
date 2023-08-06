#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import click
from ckanext.attribution.lib.orcid_api import OrcidApi
from ckanext.attribution.lib.ror_api import RorApi
from prompt_toolkit import prompt
from nameparser import HumanName

from .common import multi_choice


class APISearch(object):
    """
    Search for a contributor on an external API and download any relevant details.
    """

    def __init__(self):
        self.api = {'ORCID': OrcidApi(), 'ROR': RorApi()}

    def update(self, contrib):
        if contrib['agent_type'] == 'person':
            api_func = self.search_orcid
        elif contrib['agent_type'] == 'org':
            api_func = self.search_ror
        else:
            api_func = None
        if api_func is not None:
            from_api = api_func(contrib)
            if from_api is not None:
                contrib.update(from_api)
        contrib['key'] = self._get_key(contrib)
        return contrib

    def _search_api(self, contrib, lookup, api_name, result_format):
        """
        Search an API endpoint for a contributor.

        :param contrib: the full contributor dict
        :param lookup: dict of query params (plus display_name) to send to api.search
        :param api_name: name of the API (see self.api)
        :param result_format: display format of each result, e.g. "{name} ({location})"
        :return: None if not found, dict for matching result if found/selected
        """
        aff = '; '.join(contrib.get('affiliations', []))
        api = self.api[api_name]
        display_name = lookup.pop('display_name')
        try:
            question = (
                f'Do any of these {api_name} results match "{display_name}" ({aff})?'
            )
            click.echo(f'\nSearching {api_name} for "{display_name}"...')
            results = api.search(**lookup).get(u'records', [])
            if len(results) > 0:
                i = multi_choice(
                    question,
                    [result_format.format(**r) for r in results] + ['None of these'],
                    default=len(results),
                )
                if i == len(results):
                    update_dict = self._manual_edit(contrib, api_name)
                else:
                    update_dict = results[i]
            else:
                click.echo(f'No results found for "{display_name}".')
                if click.confirm('Try with a different name?'):
                    new_name = prompt('New name to search: ', default=display_name)
                    if contrib['agent_type'] == 'person':
                        new_name = HumanName(new_name)
                        lookup['family_name'] = new_name.last
                        lookup['given_names'] = new_name.first
                        contrib['family_name'] = new_name.last
                        contrib['given_names'] = new_name.first
                    else:
                        lookup['q'] = new_name
                        lookup['name'] = new_name
                    lookup['display_name'] = self._get_key(contrib)
                    update_dict = self._search_api(
                        contrib, lookup, api_name, result_format
                    )
                else:
                    update_dict = self._manual_edit(contrib, api_name)
        except Exception as e:
            click.echo(f'{api_name} search error for "{display_name}"', err=True)
            click.echo(e, err=True)
            update_dict = self._manual_edit(contrib, api_name)
        update_dict['agent_type'] = contrib['agent_type']
        if 'name' in update_dict or 'family_name' in update_dict:
            new_name = self._get_key(update_dict)
            click.echo(f'Setting name to {new_name}')
        return update_dict

    def _manual_edit(self, contrib, api_name):
        if click.confirm('Enter ID manually?'):
            api = self.api[api_name]
            _id = click.prompt(f'{api_name} ID', show_default=False).strip()
            return api.as_agent_record(api.read(_id))
        if not click.confirm('Edit names manually?'):
            return {}
        if contrib.get('agent_type') == 'person':
            return {
                'given_names': prompt('Given names: ', default=contrib['given_names']),
                'family_name': prompt('Family name: ', default=contrib['family_name']),
            }
        else:
            return {'name': prompt('Name: ', default=contrib['name'])}

    def search_orcid(self, contrib):
        display_name = ' '.join([contrib['given_names'], contrib['family_name']])
        result_format = '{family_name}, {given_names} ({external_id})'
        lookup = {
            'display_name': display_name,
            'family_name': contrib['family_name'],
            'given_names': contrib['given_names'],
        }
        return self._search_api(contrib, lookup, 'ORCID', result_format)

    def search_ror(self, contrib):
        result_format = '{name}, {location} ({external_id})'
        lookup = {'display_name': contrib['name'], 'q': contrib['name']}
        return self._search_api(contrib, lookup, 'ROR', result_format)

    def _get_key(self, contrib_dict):
        if contrib_dict['agent_type'] == 'person':
            return contrib_dict['family_name'] + ', ' + contrib_dict['given_names']
        else:
            return contrib_dict['name']
