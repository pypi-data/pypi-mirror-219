#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckantools.decorators import auth
from ckantools.vars import auth_valid


@auth()
def agent_affiliation_create(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid


@auth()
def agent_create(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid


@auth()
def contribution_activity_create(context, data_dict):
    """
    Allow for logged-in users.
    """
    return auth_valid
