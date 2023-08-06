#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckanext.attribution.model.contribution_activity import (
    ContributionActivity,
    contribution_activity_table,
)

from ._base import BaseQuery


class ContributionActivityQuery(BaseQuery):
    """
    
    """

    # model and table (subclasses should override)
    m = ContributionActivity
    t = contribution_activity_table
