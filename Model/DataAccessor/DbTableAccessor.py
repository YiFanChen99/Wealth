# -*- coding: utf-8 -*-
from peewee import *

from Model.DataAccessor.DbAccessor.DbOrmAccessor import db, BaseModel


class SubjectType(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return self.name


class SubjectRegion(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return self.name


class TransactionType(BaseModel):
    name = TextField(unique=True)

    def __repr__(self):
        return self.name


class Account(BaseModel):
    description = TextField()
    balance = FloatField(default=0)
    currency = TextField()
    commission_rule = TextField()


class Subject(BaseModel):
    code = TextField(unique=True)
    type = ForeignKeyField(SubjectType, backref='_subject')
    region = ForeignKeyField(SubjectRegion, backref='_subject')
    currency = TextField()


class Transaction(BaseModel):
    date = DateField()
    type = ForeignKeyField(TransactionType, backref='_transaction')
    account = ForeignKeyField(Account, backref='_transaction')
    subject = ForeignKeyField(Subject, backref='_transaction')
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
