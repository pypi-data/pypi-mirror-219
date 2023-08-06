#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from ckanext.attribution.model.package_contribution_activity import (
    PackageContributionActivity,
    package_contribution_activity_table,
)
from ckan.model import Session
from ._base import BaseQuery


class PackageContributionActivityQuery(BaseQuery):
    """
    
    """

    # model and table (subclasses should override)
    m = PackageContributionActivity
    t = package_contribution_activity_table

    @classmethod
    def read_package(cls, pkg_id):
        return (
            Session.query(PackageContributionActivity)
            .filter(PackageContributionActivity.package_id == pkg_id)
            .all()
        )
