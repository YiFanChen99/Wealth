#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *

from Model.DataAccessor.DbAccessor.DbOrmAccessor import BaseModel, SimpleModelMap
from Model.DbRecordModel.Utility import TransactionSummary
from Model.Currency import create_currency


class SubjectType(BaseModel):
    name = TextField(unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class SubjectRegion(BaseModel):
    name = TextField(unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Subject(BaseModel):
    code = TextField(unique=True)
    name = TextField(null=True)
    type = ForeignKeyField(SubjectType, backref='subject_')
    region = ForeignKeyField(SubjectRegion, backref='subject_')
    currency_code = TextField()
    is_fund = BooleanField()

    # noinspection PyTypeChecker
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currency = create_currency(self.currency_code)
        self.summary = None
        self.update_summary()

    @property
    def transactions(self):
        return sorted(self.transaction_, key=lambda tr: tr.date)

    @property
    def accounts(self):
        return set(trans.account for trans in self.transactions)

    @property
    def holding(self):
        return self.summary.net_amount

    @property
    def is_holding(self):
        return self.holding > 0.1

    @property
    def avg_cost(self):
        return self.summary.avg_price

    def update_summary(self):
        self.summary = TransactionSummary(self.transactions)


def _create_tables():
    """
    Peewee will create tables in all-lowercases.
    """
    from Model.DataAccessor.DbAccessor.DbOrmAccessor import db
    db.create_tables([SubjectType, SubjectRegion, Subject])


TYPE_MAP = SimpleModelMap(SubjectType)
REGION_MAP = SimpleModelMap(SubjectRegion)
