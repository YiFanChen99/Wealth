#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.DbRecordModel.BaseModel import BaseRecordModel, SimpleModelMap
from Model.DbRecordModel.Utility import TransactionSummarizer
from Model.DataAccessor.DbTableAccessor import Subject, SubjectType, SubjectRegion
from Model.Currency import create_currency


TYPE_MAP = SimpleModelMap(SubjectType)
REGION_MAP = SimpleModelMap(SubjectRegion)


class SubjectModel(BaseRecordModel):
    ACCESSOR = Subject

    @classmethod
    def create_record(cls, code, type_, region, currency):
        rec = cls(code, type_, region, currency)
        rec.sync_to_db()
        return rec

    def _init_by_record(self, record):
        self._init_by_args(iter((record.code, record.type, record.region, record.currency)))

    def _init_by_args(self, iterator):
        self.code = next(iterator)
        self.type = TYPE_MAP.get_record(next(iterator))
        self.region = REGION_MAP.get_record(next(iterator))
        self.currency = create_currency(next(iterator))

    def _get_sync_kwargs(self):
        return {
            'code': self.code, 'type': self.type,
            'region': self.region, 'currency': self.currency.code
        }

    @property
    def transactions(self):
        if self.record is None:
            raise ValueError("Non-created Account.")
        return self.record.transactions

    @property
    def accounts(self):
        if self.record is None:
            raise ValueError("Non-created Account.")
        return self.record.accounts

    @property
    def holding(self):
        result = TransactionSummarizer(self.transactions)
        return result.net_amount
