#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *

from Model.DataAccessor.DbAccessor.DbOrmAccessor import BaseModel, SimpleModelMap
from Model.DbRecordModel.Utility import TransactionSummarizer
from Model.Currency import create_currency


class SubjectType(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return repr(self.name)


class SubjectRegion(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return repr(self.name)


class Subject(BaseModel):
    code = TextField(unique=True)
    type = ForeignKeyField(SubjectType, backref='subject_')
    region = ForeignKeyField(SubjectRegion, backref='subject_')
    currency_code = TextField()

    # noinspection PyTypeChecker
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currency = create_currency(self.currency_code)

    @property
    def transactions(self):
        return self.transaction_

    @property
    def accounts(self):
        return set(trans.account for trans in self.transactions)

    @property
    def holding(self):
        result = TransactionSummarizer(self.transactions)
        return result.net_amount


def _create_tables():
    """
    Peewee will create tables in all-lowercases.
    """
    from Model.DataAccessor.DbAccessor.DbOrmAccessor import db
    db.create_tables([SubjectType, SubjectRegion, Subject])


TYPE_MAP = SimpleModelMap(SubjectType)
REGION_MAP = SimpleModelMap(SubjectRegion)
