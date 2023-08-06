#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import itertools
import re

import click
from ckanext.attribution.lib.orcid_api import OrcidApi
from ckanext.attribution.lib.ror_api import RorApi
from fuzzywuzzy import process
from prompt_toolkit import prompt
from unidecode import unidecode

from .common import multi_choice


class Combiner(object):
    """
    Combines names extracted by a Parser.
    """

    def __init__(self, parser):
        self.contributors = parser.contributors
        self.affiliations = parser.affiliations

    def separate(self, group):
        """
        Ensure that the automated grouping is correct.

        :param group: a list of ParsedSegment instances that are probably the same contributor
        :return: a list of lists of ParsedSegments
        """
        all_names = sorted(
            list(set([str(x.name) for x in group])), key=lambda x: -len(x)
        )
        if len(all_names) > 1:
            same = click.confirm(
                'Are these all the same contributor?\n\t{0}\n'.format(
                    '\n\t'.join(all_names)
                ),
                default=True,
            )
            if not same:
                subgroups = {}
                for n in all_names:
                    v = [x for x in group if x.name == n]
                    if len(subgroups) == 0:
                        subgroups[n] = v
                        continue
                    matches = [m[0] for m in process.extract(n, list(subgroups.keys()))]
                    ix = multi_choice(
                        'Is "{0}" the same as any of these contributors?'.format(n),
                        matches + ['None of these'],
                        default=len(matches),
                    )
                    k = matches[ix] if ix < len(matches) else n
                    subgroups[k] = subgroups.get(k, []) + v
                return list(subgroups.values())
        return [group]

    def combine(self, group, agent_type, name_func=None):
        all_names = [x.name for x in group]
        _contrib_dicts = sorted(
            [(ct, pkgs) for c in group for ct, pkgs in c.packages.items()],
            key=lambda x: x[0],
        )
        _grouped_contribs = itertools.groupby(_contrib_dicts, key=lambda x: x[0])
        contrib = {
            'agent_type': agent_type,
            'all_names': [str(n) for n in all_names],
            'affiliations': list(set([a for x in group for a in x.affiliations])),
            'packages': {
                contrib_type: list(set([pkgid for ct, pkgid in v]))
                for contrib_type, v in _grouped_contribs
            },
        }
        if name_func is None:
            longest_name = sorted(list(set(all_names)), key=lambda x: -len(x))[
                0
            ].strip()
            name = {'name': longest_name}
        else:
            name = name_func(all_names)
        contrib.update(name)
        contrib['key'] = self._get_key(contrib)
        return contrib

    def combine_person_names(self, names):
        """
        Uses a list of HumanNames to determine the longest possible name for a person.

        :return: a dict of family_name, given_names (includes middle names), and key (i.e. a sort/display name)
        """

        def _filter_diacritics(name_list):
            filtered = [n for n in name_list if unidecode(n) != n]
            if len(filtered) > 0:
                return filtered
            else:
                return name_list

        given = []
        family = []
        for n in names:
            given.append(' '.join([n.first, n.middle]))
            family.append(n.last)
        given = list(set(given))
        family = list(set(family))

        # use longest family name
        family_name = sorted(_filter_diacritics(family), key=lambda x: -len(x))[
            0
        ].strip()
        # given names are more complicated
        # remove empty strings and split into parts
        given = [re.split(r'\s+', m) for m in list(set(given)) if m != '']
        given_parts = {}
        for m in given:
            for i, x in enumerate(m):
                given_parts[i] = given_parts.get(i, []) + [x]
        given_names = ' '.join(
            [
                sorted(_filter_diacritics(p), key=lambda x: -len(x))[0]
                for p in given_parts.values()
            ]
        ).strip()
        combined = {'family_name': family_name, 'given_names': given_names}
        return combined

    def update_affiliations(self, contributor):
        """
        Update the self.affiliations dict to ensure the names are consistent.

        :param contributor: contributor dict
        """
        no_affiliations = len(contributor.get('affiliations', [])) == 0
        is_not_affiliation = len(contributor['packages'].get('affiliations', [])) == 0
        if no_affiliations and is_not_affiliation:
            return
        all_packages = [
            pkg_id for x in contributor['packages'].values() for pkg_id in x
        ]
        for pkg in all_packages:
            items = self.affiliations.get(pkg[0])
            if items is None:
                continue
            updated_items = []
            for name, affiliation in items:
                if name in contributor['all_names']:
                    updated_items.append((contributor['key'], affiliation))
                elif affiliation in contributor['all_names']:
                    updated_items.append((name, contributor['key']))
                else:
                    updated_items.append((name, affiliation))
            self.affiliations[pkg[0]] = updated_items

    def run(self):
        """
        Run the combiner over the whole parser list, including separating groups,
        combining names, searching APIs, and updating the affiliations dict.

        :return: a list of contributors
        """
        combined = []

        for g in [
            grp
            for family_name, initials_list in self.contributors['person'].items()
            for initial, grp in initials_list.items()
        ]:
            for person in self.separate(g):
                c = self.combine(person, 'person', self.combine_person_names)
                if c is not None:
                    combined.append(c)
                    self.update_affiliations(c)
        for abbr, g in self.contributors['org'].items():
            for org in self.separate(g):
                c = self.combine(org, 'org', None)
                if c is not None:
                    combined.append(c)
                    self.update_affiliations(c)
        for abbr, g in self.contributors['other'].items():
            for o in self.separate(g):
                c = self.combine(o, 'other')
                if c is not None:
                    combined.append(c)
                    self.update_affiliations(c)
        return combined

    def _get_key(self, contrib_dict):
        if contrib_dict['agent_type'] == 'person':
            return contrib_dict['family_name'] + ', ' + contrib_dict['given_names']
        else:
            return contrib_dict['name']
