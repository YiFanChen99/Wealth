#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseRecordModel(object):
    ACCESSOR = None

    def __init__(self, *args):
        if isinstance(args[0], self.ACCESSOR):
            self.record = args[0]
            self._init_by_record(self.record)
        else:
            self.record = None
            self._init_by_args(iter(args))

    def _init_by_record(self, record):
        raise NotImplementedError

    def _init_by_args(self, iterator):
        raise NotImplementedError

    def sync_to_db(self):
        self.record = self.ACCESSOR.replace(id=self.id, **self._get_sync_kwargs()).execute()

    def _get_sync_kwargs(self):
        raise NotImplementedError

    @property
    def id(self):
        return None if self.record is None else self.record.id

    @classmethod
    def get(cls, **kwargs):
        if cls.ACCESSOR is None:
            raise NotImplementedError
        return cls(cls.ACCESSOR.get(**kwargs))


class SimpleModelMap(object):
    def __init__(self, accessor):
        if accessor is None:
            raise TypeError

        self._accessor = accessor
        self.map = {record.id: record for record in accessor.select()}

    def get_record(self, record_or_id):
        if isinstance(record_or_id, self._accessor):
            return record_or_id
        elif isinstance(record_or_id, int):
            return self.map[record_or_id]
        else:
            raise TypeError

    def __repr__(self):
        return repr(self.map)
