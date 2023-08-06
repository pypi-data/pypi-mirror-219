#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-dataset-contributors
# Created by the Natural History Museum in London, UK

import click
from ckan.model import Session
from ckan.model.package_extra import PackageExtra
from ckan.plugins import toolkit
from ckanext.attribution.commands import migration
from ckanext.attribution.logic.actions.helpers import get_author_string
from ckanext.attribution.model import (
    agent,
    agent_affiliation,
    agent_contribution_activity,
    contribution_activity,
    package_contribution_activity,
    relationships,
)
from ckanext.attribution.model.crud import (
    AgentQuery,
    PackageQuery,
    PackageContributionActivityQuery,
    AgentAffiliationQuery,
    AgentContributionActivityQuery,
)
from fuzzywuzzy import process, fuzz
from sqlalchemy import and_, or_


def get_commands():
    return [attribution]


@click.group()
def attribution():
    """
    Commands for the ckanext-attribution plugin.
    """
    pass


@attribution.command()
def initdb():
    """
    Create database tables required for this extension.
    """
    contribution_activity.check_for_table()
    agent.check_for_table()
    agent_affiliation.check_for_table()
    agent_contribution_activity.check_for_table()
    package_contribution_activity.check_for_table()
    relationships.setup_relationships()


@attribution.command()
@click.argument('ids', nargs=-1)
def sync(ids):
    """
    Pull updated details for agents from external services like ORCID and ROR.

    Only applies when an external_id has already been set.
    """
    agent_external_update = toolkit.get_action('agent_external_update')
    if not ids:
        ids = [a.id for a in AgentQuery.all() if a.external_id]
    click.echo('Attempting to sync {0} records.'.format(len(ids)))
    errors = []
    with click.progressbar(ids) as bar:
        for _id in bar:
            try:
                agent_external_update({'ignore_auth': True}, {'id': _id})
            except Exception as e:
                errors.append('Error ({0}): {1}'.format(_id, e))
    failed = len(errors)
    total = len(ids)
    click.echo('Updated {0}/{1} ({2} failed)'.format(total - failed, total, failed))
    for e in errors:
        click.echo(e, err=True)


@attribution.command()
@click.argument('ids', nargs=-1)
def refresh_packages(ids):
    """
    Update the author string for all (or the specified) packages.
    """
    if not ids:
        ids = list(set([r.package_id for r in PackageContributionActivityQuery.all()]))
    click.echo(
        'Attempting to update the author field for {0} packages.'.format(len(ids))
    )
    errors = []
    with click.progressbar(ids) as bar:
        for _id in bar:
            try:
                authors = get_author_string(package_id=_id)
                PackageQuery.update(_id, author=authors)
            except Exception as e:
                errors.append('Error ({0}): {1}'.format(_id, e))
    failed = len(errors)
    total = len(ids)
    click.echo('Updated {0}/{1} ({2} failed)'.format(total - failed, total, failed))
    for e in errors:
        click.echo(e, err=True)


@attribution.command()
@click.argument('ids', nargs=-1)
@click.option(
    '--limit', help='Process n packages at a time (best for testing/debugging).'
)
def agent_external_search(ids, limit):
    if ids:
        agents = AgentQuery.search(AgentQuery.m.id.in_(ids))
    else:
        agents = AgentQuery.search(AgentQuery.m.external_id.is_(None))
    agents = sorted(agents, key=lambda x: -len(x.contribution_activities))
    if limit:
        agents = agents[: int(limit)]
    total = len(agents)
    click.echo(f'{total} contributors without external IDs found.')
    updater = migration.APISearch()
    for i, a in enumerate(agents):
        click.echo(f'Searching {i} of {total}')
        update_dict = updater.update(a.as_dict())
        AgentQuery.update(a.id, **update_dict)


@attribution.command()
@click.option('--q')
@click.option('--match-threshold', default=75)
def merge_agents(q, match_threshold):
    agents = toolkit.get_action('agent_list')({}, {'q': q})
    all_agents = AgentQuery.all()
    merging = []
    for a in agents:
        if a['id'] in merging:
            continue
        other_agents = [o.display_name for o in all_agents if o.id != a['id']]
        compare = process.extract(
            a['display_name'], other_agents, limit=10, scorer=fuzz.token_set_ratio
        )
        matches = [m for m in compare if m[1] >= int(match_threshold)]
        to_merge = []
        while matches:
            ix = migration.multi_choice(
                f'Choose a{"nother" if len(to_merge) > 0 else ""} record to merge with {a["display_name"]}:',
                [f'{m}: {x}%' for m, x in matches] + ['None of these'],
                default=len(matches),
            )
            if ix == len(matches):
                break
            match_name = matches.pop(ix)[0]
            to_merge.append(
                next(
                    r
                    for r in all_agents
                    if r.display_name == match_name and r.id != a['id']
                )
            )
        if len(to_merge) == 0:
            continue
        to_merge.append(AgentQuery.read(a['id']))
        merging += [m.id for m in to_merge]
        has_external_id = [r for r in to_merge if r.external_id is not None]
        if len(has_external_id) == 1:
            base_record = has_external_id[0]
        else:
            choices = has_external_id if len(has_external_id) > 1 else to_merge
            ix = migration.multi_choice(
                'Choose base record:',
                [f'{r.display_name} ({r.external_id_url or "no ID"})' for r in choices],
            )
            base_record = choices[ix]
        not_base_record = [r for r in to_merge if r.id != base_record.id]
        for merging_record in not_base_record:
            # update affiliations
            for aff in merging_record.affiliations:
                if aff['agent'].id == base_record.id:
                    AgentAffiliationQuery.delete(aff['affiliation'].id)
                else:
                    k = (
                        'agent_a_id'
                        if aff['affiliation'].agent_a_id == merging_record.id
                        else 'agent_b_id'
                    )
                    AgentAffiliationQuery.update(
                        aff['affiliation'].id, **{k: base_record.id}
                    )
            base_record_activities = AgentContributionActivityQuery.search(
                AgentContributionActivityQuery.m.agent_id == base_record.id
            )
            merging_activities = AgentContributionActivityQuery.search(
                AgentContributionActivityQuery.m.agent_id == merging_record.id
            )
            for activity in merging_activities:
                name = activity.contribution_activity.activity
                pkg = activity.contribution_activity.package.id
                scheme = activity.contribution_activity.scheme
                matching_activities = [
                    x
                    for x in base_record_activities
                    if (
                        x.contribution_activity.activity == name
                        and x.contribution_activity.package.id == pkg
                        and x.contribution_activity.scheme == scheme
                    )
                ]
                if len(matching_activities) == 0:
                    AgentContributionActivityQuery.update(
                        activity.id, agent_id=base_record.id
                    )
                else:
                    matching_activities.append(activity)
                    matching_activities = sorted(
                        matching_activities, key=lambda x: x.contribution_activity.order
                    )
                    first_activity = matching_activities.pop(0)
                    AgentContributionActivityQuery.update(
                        first_activity.id, agent_id=base_record.id
                    )
                    for other_activity in matching_activities:
                        AgentContributionActivityQuery.delete(other_activity.id)
            AgentQuery.delete(merging_record.id)
            click.echo(
                f'Merged {merging_record.display_name} ({merging_record.id}) into {base_record.display_name} ({base_record.id}).'
            )
    if len(merging) == 0:
        click.echo('Nothing to merge.')


@attribution.command()
@click.option(
    '--limit', help='Process n packages at a time (best for testing/debugging).'
)
@click.option('--dry-run', help='Don\'t save anything to the database.', is_flag=True)
@click.option(
    '--search-api/--no-search-api',
    help='Search external APIs (e.g. ORCID) for details.',
    default=True,
)
def migratedb(limit, dry_run, search_api):
    """
    Semi-manual migration script that attempts to extract individual contributors from
    'author' and 'contributor' fields (if present) in order to create Agent and
    ContributionActivity records for them.
    """
    if not dry_run:
        click.secho(
            'Attempting to migrate contributors. It is HIGHLY recommended that you back up your '
            'database before running this.',
            fg='red',
        )
        click.confirm('Continue?', default=False, abort=True)
    converted_packages = [r.package_id for r in PackageContributionActivityQuery.all()]
    unconverted_packages = PackageQuery.search(
        ~PackageQuery.m.id.in_(converted_packages)
    )
    contribution_extras = {
        p.id: Session.query(PackageExtra)
        .filter(PackageExtra.package_id == p.id, PackageExtra.key == 'contributors')
        .first()
        for p in unconverted_packages
    }
    total = len(unconverted_packages)
    limit = int(limit or total)
    parser = migration.Parser()

    for i, pkg in enumerate(unconverted_packages[:limit]):
        click.echo('Processing package {0} of {1}.\n'.format(i + 1, total))
        parser.run(pkg.author, pkg.id, 'author')
        if contribution_extras.get(pkg.id) is not None:
            extras = contribution_extras.get(pkg.id).value
            if not isinstance(extras, str):
                parser.run(extras, pkg.id, 'contributor')

    combiner = migration.Combiner(parser)
    combined = combiner.run()
    if search_api:
        api_updater = migration.APISearch()
        for agnt in combined:
            api_updater.update(agnt)
    click.echo(f'\n\n{len(combined)} contributors found.')
    if dry_run:
        click.echo('Exiting before saving to the database.')
        return
    agent_lookup = {}
    agent_create = toolkit.get_action('agent_create')
    contribution_activity_create = toolkit.get_action('contribution_activity_create')
    agent_affiliation_create = toolkit.get_action('agent_affiliation_create')
    remove_keys = ['packages', 'affiliations', 'key', 'all_names']
    for a in combined:
        try:
            # create the agent (check it doesn't exist first)
            agent_dict = {**{k: v for k, v in a.items() if k not in remove_keys}}
            if a['agent_type'] == 'person':
                filters = [
                    and_(
                        AgentQuery.m.family_name == a['family_name'],
                        AgentQuery.m.given_names == a['given_names'],
                    )
                ]
            else:
                filters = [AgentQuery.m.name == a['name']]
            if a.get('external_id'):
                filters.append(AgentQuery.m.external_id == a.get('external_id'))
            matches = AgentQuery.search(or_(*filters))
            if len(matches) == 1:
                new_agent = matches[0].as_dict()
                click.echo(f'MATCHED "{a["key"]}"')
            elif len(matches) > 1:
                choice_ix = migration.multi_choice(
                    f'Does "{a["key"]}" match any of these existing agents?',
                    [m.display_name for m in matches] + ['None of these'],
                )
                if choice_ix == len(matches):
                    del a['external_id']
                    del a['external_id_scheme']
                    new_agent = agent_create({'ignore_auth': True}, agent_dict)
                    click.echo(f'CREATED "{a["key"]}"')
                else:
                    new_agent = matches[choice_ix].as_dict()
                    click.echo(f'MATCHED "{a["key"]}"')
            else:
                new_agent = agent_create({'ignore_auth': True}, agent_dict)
                click.echo(f'CREATED "{a["key"]}"')
            agent_lookup[a['key']] = new_agent['id']
            # then activities
            for pkg, order in a['packages'].get('author', []):
                # create citation
                contribution_activity_create(
                    {'ignore_auth': True},
                    {
                        'activity': '[citation]',
                        'scheme': 'internal',
                        'order': order,
                        'package_id': pkg,
                        'agent_id': new_agent['id'],
                    },
                )
                # then the actual activity
                contribution_activity_create(
                    {'ignore_auth': True},
                    {
                        'activity': 'Unspecified',
                        'scheme': 'internal',
                        'package_id': pkg,
                        'agent_id': new_agent['id'],
                    },
                )
            for pkg, _ in a['packages'].get('contributor', []):
                # just the activity for this one
                contribution_activity_create(
                    {'ignore_auth': True},
                    {
                        'activity': 'Unspecified',
                        'scheme': 'internal',
                        'package_id': pkg,
                        'agent_id': new_agent['id'],
                    },
                )
        except Exception as e:
            # very broad catch just so it doesn't ruin everything if one thing breaks
            click.echo(f'Skipping {a["key"]} due to error: {e}', err=True)
    # finally, the affiliations
    for pkg, pairs in combiner.affiliations.items():
        for agent_a, agent_b in pairs:
            try:
                agent_affiliation_create(
                    {'ignore_auth': True},
                    {
                        'agent_a_id': agent_lookup[agent_a],
                        'agent_b_id': agent_lookup[agent_b],
                        'package_id': pkg,
                    },
                )
            except Exception as e:
                # very broad catch just so it doesn't ruin everything if one thing breaks
                click.echo(
                    f'Skipping {agent_a} + {agent_b} affiliation due to error: {e}',
                    err=True,
                )

    # finally finally, update the package author strings
    for pkg in unconverted_packages[:limit]:
        try:
            authors = get_author_string(package_id=pkg.id)
            PackageQuery.update(pkg.id, author=authors)
        except Exception as e:
            # very broad catch just so it doesn't ruin everything if one thing breaks
            click.echo(f'Skipping {pkg.id} due to error: {e}', err=True)
