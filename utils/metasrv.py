#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(current_app)


class MetaService(object):
    def __init__(self, model):
        '''
        初始化
        '''
        self._model = model

    def insert(self, row_dict):
        row = self._model(**row_dict)
        db.session.add(row)
        db.session.commit()
        return row.id

    def insert_all(self, row_list):
        row_list_ = []
        for row in row_list:
            row_list_.append(self._model(**row))
        db.session.add_all(row_list_)
        db.session.commit()
        return row_list_

    def delete(self, row_id, soft=False):
        row = self._model.query.get(row_id)
        if soft:
            row.is_delete = 1
        else:
            db.session.delete(row)
        db.session.commit()
        return None

    def update(self, row_id, row_dict):
        self._assert_dict_not_empty(row_dict)
        row = self._model.query.get(row_id)

        for key, value in row_dict.iteritems():
            if value is not None:
                setattr(row, key, value)

        db.session.commit()
        return row

    def update_all(self, params, row_dict):
        self._assert_dict_not_empty(row_dict)

        row_dict_ = {}
        for key, value in row_dict.iteritems():
            if value is not None:
                setattr(row_dict_, key, value)

        self._model.query.filter_by(**params).update(row_dict_)
        db.session.commit()
        return None

    def read(self, row_id):
        row = self._model.query.get(row_id)
        return row

    def read_list(self, params, page=1, psize=20, orderby=None):
        orderby = orderby or []
        query = self._model.query

        for key, value in params.iteritems():
            if value is None:
                continue
            if isinstance(value, (list, set, tuple)):
                query = query.filter(key.in_(list(value)))
            else:
                query = query.filter_by(key=value)

        count = query.count()

        if count == 0:
            return {"count": 0, "list": []}

        if page and psize:
            query = query.offset((page - 1) * psize).limit(psize)

        for field, direction in orderby:
            query = query.order_by('%s %s' % (field, direction))

        return {
            "count": count,
            "list": query.all()
        }

    def read_all(self, params, page=1, psize=20, orderby=None):
        orderby = orderby or []
        query = self._model.query

        for key, value in params.iteritems():
            if value is None:
                continue
            if isinstance(value, (list, set, tuple)):
                query = query.filter(key.in_(list(value)))
            else:
                query = query.filter_by(key=value)

        for field, direction in orderby:
            query = query.order_by('%s %s' % (field, direction))

        return query.all()

    def _assert_dict_not_empty(self, row_dict):
        assert isinstance(row_dict, dict) and row_dict, "row_dict must be a dict and can't be empty"
