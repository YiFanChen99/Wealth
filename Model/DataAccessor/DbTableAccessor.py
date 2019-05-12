# -*- coding: utf-8 -*-
from peewee import *

from Model.DataAccessor.DbAccessor.DbOrmAccessor import db, BaseModel


class SubjectType(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return repr(self.name)


class SubjectRegion(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return repr(self.name)


class TransactionType(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return repr(self.name)


class Account(BaseModel):
    description = TextField()
    value = FloatField(default=0)
    currency = TextField()
    commission_rule = TextField()

    @property
    def transactions(self):
        return self.transaction_

    @property
    def subjects(self):
        return set(trans.subject for trans in self.transactions)


class Subject(BaseModel):
    code = TextField(unique=True)
    type = ForeignKeyField(SubjectType, backref='subject_')
    region = ForeignKeyField(SubjectRegion, backref='subject_')
    currency = TextField()

    @property
    def transactions(self):
        return self.transaction_

    @property
    def accounts(self):
        return set(trans.account for trans in self.transactions)


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
    Needs to be renamed manually in camel-style.
    """
    db.create_tables([SubjectType, SubjectRegion, TransactionType])
    db.create_tables([Account, Subject, Transaction])
