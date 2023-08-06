#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckantools.decorators import auth
from ckantools.vars import auth_valid

from ckan.authz import is_sysadmin


@auth()
def agent_affiliation_delete(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid


@auth()
def agent_delete(context, data_dict):
    """
    Only allow for sysadmins (who usually skip this method, except in tests).
    """
    return {'success': is_sysadmin(context.get('user'))}


@auth()
def agent_contribution_activity_delete(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid


@auth()
def contribution_activity_delete(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid


@auth()
def package_contribution_activity_delete(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid
