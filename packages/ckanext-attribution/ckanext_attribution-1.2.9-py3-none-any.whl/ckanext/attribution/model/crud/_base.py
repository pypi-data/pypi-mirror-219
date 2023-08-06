#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-attribution
# Created by the Natural History Museum in London, UK

from abc import ABCMeta
from ckan.model import DomainObject, Session
from sqlalchemy import Table
from ckan.plugins import toolkit


class BaseQuery(object):
    """
    A base class for easy CRUD (create, read, update, delete) access to attribution
    models.
    """

    __metaclass__ = ABCMeta

    #: :type: The associated database model type.
    m = DomainObject

    #: :sqlalchemy.Table: The associated database table instance
    t = Table()

    @classmethod
    def _columns(cls, **kwargs):
        '''


        :param kwargs:

        '''
        return {c.name: kwargs.get(c.name) for c in cls.t.c if c.name in kwargs}

    @classmethod
    def validate(cls, data_dict):
        """
        Ensure the data_dict provided contains the correct parameters for creating or
        updating a record, and fix issues where possible by deleting extra fields.

        :param data_dict: a complete dictionary of parameters that will be passed to :func:`create`
                          or :func:`update`
        :type data_dict: dict
        :returns: updated data_dict if valid, raises error if not
        """

        def _empty_string_to_null(item):
            if isinstance(item, list):
                return [_empty_string_to_null(i) for i in item]
            if isinstance(item, dict):
                return {k: _empty_string_to_null(v) for k, v in item.items()}
            if item == '':
                return None
            return item

        data_dict = cls._columns(**_empty_string_to_null(data_dict))

        if 'id' in data_dict:
            existing_record = cls.read(data_dict.get('id'))
            if existing_record is None:
                return data_dict
            for c in cls.t.c:
                if c.name not in data_dict:
                    data_dict[c.name] = getattr(existing_record, c.name)

        return data_dict

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new record of type :class:`~m`.
        """
        item_dict = cls._columns(**kwargs)
        new_item = cls.m(**item_dict)
        Session.add(new_item)
        Session.commit()
        return new_item

    @classmethod
    def read(cls, item_id):
        """
        Retrieve a record of type :class:`~m` by its ID.

        :param item_id: the ID of the record.
        :type item_id: str
        """
        retrieved_item = Session.query(cls.m).get(item_id)
        if retrieved_item is None:
            raise toolkit.ObjectNotFound('{0} was not found.'.format(item_id))
        return retrieved_item

    @classmethod
    def exists(cls, item_id):
        """
        Check if a record with the given ID exists.

        :param item_id: the ID of the potential record
        :return: bool
        """
        return Session.query(cls.m).get(item_id) is not None

    @classmethod
    def search(cls, query):
        """
        Retrieve all records matching the search criteria.

        :param query: a sqlalchemy filter query
        """
        return Session.query(cls.m).filter(query).all()

    @classmethod
    def all(cls):
        """
        Return all records.
        """
        return Session.query(cls.m).all()

    @classmethod
    def update(cls, item_id, **kwargs):
        '''


        :param item_id:
        :param kwargs:

        '''
        try:
            del kwargs['id']
        except KeyError:
            pass
        retrieved_item = Session.query(cls.m).filter(cls.m.id == item_id)
        if retrieved_item.count() < 1:
            raise toolkit.ObjectNotFound('{0} was not found.'.format(item_id))
        retrieved_item.update(cls._columns(**kwargs))
        Session.commit()
        return Session.query(cls.m).get(item_id)

    @classmethod
    def delete(cls, item_id):
        '''


        :param item_id:

        '''
        to_delete = Session.query(cls.m).get(item_id)
        if to_delete is not None:
            Session.delete(to_delete)
            Session.commit()
