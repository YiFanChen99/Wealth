#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *
from datetime import date

from Model.DataAccessor.DbAccessor.DbOrmAccessor import BaseModel, SimpleModelMap
from Model.DbRecordModel.AccountModel import Account
from Model.DbRecordModel.SubjectModel import Subject


class TransactionType(BaseModel):
    name = TextField(unique=True)

    def __str__(self):
        return self.name

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

    @staticmethod
    def create_by_raws(raws):
        for raw in raws:
            Transaction.create_by_raw(*raw)

    @staticmethod
    def create_by_raw(year, month, day, type_id, account_desc, subject_code, price, amount, commission):
        date_ = date(year, month, day)
        account = Account.get(description=account_desc)
        subject = Subject.get(code=subject_code)
        Transaction.create(date=date_, type_id=type_id, account=account, subject=subject,
                           price=price, amount=amount, commission=commission)

    @classmethod
    def create(cls, **kwargs):
        trans = super().create(**kwargs)
        trans.account.update_summary()
        trans.subject.update_summary()


def _create_tables():
    """
    Peewee will create tables in all-lowercases.
    """
    from Model.DataAccessor.DbAccessor.DbOrmAccessor import db
    db.create_tables([TransactionType, Transaction])


TYPE_MAP = SimpleModelMap(TransactionType)
