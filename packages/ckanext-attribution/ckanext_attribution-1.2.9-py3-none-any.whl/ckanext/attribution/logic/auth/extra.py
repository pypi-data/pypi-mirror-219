#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK


from ckantools.decorators import auth
from ckantools.vars import auth_valid


@auth(anon=True)
def attribution_controlled_lists(context, data_dict):
    return auth_valid


@auth('agent_show')
def agent_external_search(context, data_dict):
    return auth_valid


@auth('agent_show')
def agent_external_read(context, data_dict):
    return auth_valid


@auth(anon=True)
def validate_external_id(context, data_dict):
    return auth_valid
