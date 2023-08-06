#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

import re
from types import SimpleNamespace

import click


def multi_choice(question, options, default=0):
    """
    Provide the user with a list of options.

    :return: index of the chosen option
    """
    click.echo(question)
    for i, o in enumerate(options):
        click.echo('\t({0}) {1}'.format(i + 1, o))
    answer = click.prompt('Choose an option', default=default + 1)
    try:
        answer = int(answer)
        click.echo('')
        return answer - 1
    except:
        click.echo('That wasn\'t an option.', err=True)
        return multi_choice(question, options, default)


rgx = SimpleNamespace(
    opening=re.compile(r'\('),
    closing=re.compile(r'\)'),
    initials=re.compile(r'([A-Z])\.\s*'),
    name=re.compile(r'(?:(?:,\s?)|^|and )([A-Za-z]+, [^,(]+)'),
    reversed_name=re.compile(r'([A-Z][A-Za-z\s-]+)\s+([A-Z.\s]+)(?![a-z])(?:,\s+)?'),
    has_affiliation=re.compile(r'^([^()]+)\((.+)\)$'),
    no_affiliation=re.compile(r'^([^(),;]+)$'),
    initialism=re.compile(r'^[A-Z.]+$'),
    abbr=re.compile(r'([A-Z]|(?<=[^A-Za-z])[a-z])'),
)
