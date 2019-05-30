#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math  # for eval commission_rule
from peewee import *

from Model.DataAccessor.DbAccessor.DbOrmAccessor import BaseModel
from Model.DbRecordModel.Utility import TransactionSummary
from Model.Currency import create_currency


class Account(BaseModel):
    description = TextField()
    value = FloatField(default=0)
    currency_code = TextField()
    commission_rule = TextField()

    # noinspection PyTypeChecker
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compute_commission = eval(self.commission_rule)
        self.currency = create_currency(self.currency_code)
        self.summary = None
        self.update_summary()

    @property
    def transactions(self):
        return sorted(self.transaction_, key=lambda tr: tr.date)

    @property
    def subjects(self):
        return set(trans.subject for trans in self.transactions)

    @property
    def balance(self):
        return self.value + self.summary.income

    def update_summary(self):
        self.summary = TransactionSummary(self.transactions)

    def deposit(self, amount):
        self.value += amount

    def withdraw(self, amount):
        self.value -= amount

    def __eq__(self, other):
        if isinstance(other, str):
            return self.description == other
        else:
            return super().__eq__(other)


def _create_tables():
    """
    Peewee will create tables in all-lowercases.
    """
    from Model.DataAccessor.DbAccessor.DbOrmAccessor import db
    db.create_tables([Account])
