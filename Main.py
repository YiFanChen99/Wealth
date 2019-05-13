#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date

from Model.Constant import CONFIGURE  # init db
from Model.DbRecordModel.AccountModel import Account
from Model.DbRecordModel.SubjectModel import Subject
from Model.DbRecordModel.TransactionModel import Transaction
from Model.DbRecordModel.Utility import HoldingValueSummary
from Model.Currency import NTD, USD


def create_subjects():
    sm2 = Subject.create(code='006209', name=None,
                         type_id=1, region_id=2, currency_code='NTD', is_fund=False)
    print('create_subjects end')


def create_transactions():
    ft = Account.get(id=2)
    tlt = Subject.get(code='TLT')
    Transaction.create(date=date(2019, 4, 30), type_id=2, account=ft, subject=tlt,
                       price=123.38, amount=35, commission=0)
    Transaction.create(date=date(2019, 4, 30), type_id=2, account=ft, subject=tlt,
                       price=123.41, amount=3, commission=0)
    agg = Subject.get(code='AGG')
    Transaction.create(date=date(2019, 4, 30), type_id=2, account=ft, subject=agg,
                       price=108.64, amount=18, commission=0)
    print('create_transactions end')


def create_transactions_by_raws():
    raws = [
        [2019, 5, 10, 1, "FT.", "LQD", 118.83, 10, 0]
    ]
    Transaction.create_by_raws(raws)
    print('create_transactions_by_raws end')


def print_foreign_balance():
    foreign_accounts = Account.select().where(Account.currency_code != 'NTD')
    print(tuple("{}: {:.2f}".format(acc.description, acc.balance) for acc in foreign_accounts))


def print_holding_value():
    hs = HoldingValueSummary(Subject.select())
    print("Total: {} (i.e. {})".format(
        NTD.format(hs.total_value),
        USD.format(USD.from_ntd(hs.total_value))))
    print(tuple("{}: {:.1%}".format(type_, ratio) for type_, ratio in hs.sorted_types))
    print(tuple("{}: {:.1%}".format(region, ratio) for region, ratio in hs.sorted_regions))
    print(tuple("{}: {:.1%} ({})".format(currency.code, ratio, currency.format(currency.from_ntd(value)))
                for currency, ratio, value in hs.sorted_currencies))


if __name__ == "__main__":
    print_holding_value()
    print('end')
