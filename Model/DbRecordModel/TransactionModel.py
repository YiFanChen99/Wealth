#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.DbRecordModel.BaseModel import BaseRecordModel, SimpleModelMap
from Model.DataAccessor.DbTableAccessor import Transaction, TransactionType


TYPE_MAP = SimpleModelMap(TransactionType)


class TransactionModel(BaseRecordModel):
    ACCESSOR = Transaction

    @classmethod
    def create_record(cls, date, type_, account, subject, price, amount, commission):
        rec = cls(date, type_, account, subject, price, amount, commission)
        rec.sync_to_db()
        return rec

    def _init_by_record(self, record):
        self._init_by_args(iter((record.date, record.type, record.account, record.subject,
                                 record.price, record.amount, record.commission)))

    def _init_by_args(self, iterator):
        self.date = next(iterator)
        self.type = TYPE_MAP.get_record(next(iterator))
        self.account = next(iterator)
        self.subject = next(iterator)
        self.price = next(iterator)
        self.amount = next(iterator)
        self.commission = next(iterator)

    def _get_sync_kwargs(self):
        return {
            'date': self.date, 'type': self.type, 'account': self.account, 'subject': self.subject,
            'price': self.price, 'amount': self.amount, 'commission': self.commission
        }
