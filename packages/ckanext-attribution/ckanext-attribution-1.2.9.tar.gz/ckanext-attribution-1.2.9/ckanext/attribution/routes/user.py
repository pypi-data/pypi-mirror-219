#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckan.plugins import toolkit
from flask import Blueprint
from ckanext.attribution.lib.helpers import user_contributions

blueprint = Blueprint(name='attribution_user', import_name=__name__)


@blueprint.route('/user/<username>/contributions', methods=['GET'])
def datasets(username):
    """
    Render a list of datasets that this user has contributed to.

    :param username: The username
    :return: str
    """
    try:
        toolkit.check_access('user_show', {}, {'id': username})
    except toolkit.NotAuthorized:
        toolkit.abort(403, toolkit._('Not authorized to see this page'))
    user = toolkit.get_action('user_show')(
        {'for_view': True}, {'id': username, 'include_num_followers': True}
    )
    return toolkit.render(
        'user/contributions.html',
        extra_vars=dict(contributions=user_contributions(user['id']), user_dict=user),
    )
