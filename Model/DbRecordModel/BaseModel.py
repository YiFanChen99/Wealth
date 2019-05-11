#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseRecordModel(object):
    ACCESSOR = None

    def __init__(self, *args):
        self.id = None

        if isinstance(args[0], self.ACCESSOR):
            self._init_by_record(args[0])
        else:
            self._init_by_args(iter(args))

    def _init_by_record(self, record):
        raise NotImplementedError

    def _init_by_args(self, iterator):
        raise NotImplementedError

    def sync_to_db(self):
        self.id = self.ACCESSOR.replace(id=self.id, **self._get_sync_kwargs()).execute()

    def _get_sync_kwargs(self):
        raise NotImplementedError
