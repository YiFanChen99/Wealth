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
    sub = Subject.get(code='SCHH')
    Transaction.create(date=date(2019, 5, 14), type_id=1, account=ft, subject=sub,
                       price=44.5, amount=2, commission=0)
    print('create_transactions end')


def create_transactions_by_raws():
    raws = [
        [2019, 5, 10, 1, "TD A.", "TLT", 123.4, 202, 0]
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


def print_holding_subjects():
    subs = [sub for sub in Subject.select() if sub.holding > 0.1]
    sorted_subs = sorted(iter(subs), key=lambda s: s.holding, reverse=True)
    print("\n".join(repr((s.code, s.holding, s.avg_cost)) for s in sorted_subs))


if __name__ == "__main__":
    # create_transactions()
    print_foreign_balance()
    print_holding_subjects()
    print('end')
