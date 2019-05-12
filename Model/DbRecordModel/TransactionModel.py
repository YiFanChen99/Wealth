#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *

from Model.DataAccessor.DbAccessor.DbOrmAccessor import BaseModel, SimpleModelMap
from Model.DbRecordModel.AccountModel import Account
from Model.DbRecordModel.SubjectModel import Subject


class TransactionType(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return repr(self.name)


class Transaction(BaseModel):
    date = DateField()
    type = ForeignKeyField(TransactionType, backref='transaction_')
    account = ForeignKeyField(Account, backref='transaction_')
    subject = ForeignKeyField(Subject, backref='transaction_')
    price = FloatField(default=0)
    amount = FloatField(default=0)
    commission = FloatField(default=0)


def _create_tables():
    """
    Peewee will create tables in all-lowercases.
    """
    from Model.DataAccessor.DbAccessor.DbOrmAccessor import db
    db.create_tables([TransactionType, Transaction])


TYPE_MAP = SimpleModelMap(TransactionType)
