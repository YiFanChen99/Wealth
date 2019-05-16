#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date

from Model.Constant import CONFIGURE  # init db
from Model.DbRecordModel.AccountModel import Account
from Model.DbRecordModel.SubjectModel import Subject
from Model.DbRecordModel.TransactionModel import Transaction
from Model.DbRecordModel.Utility import HoldingValueSummary
from Model.Currency import NTD, USD, create_currency


def create_subjects():
    sm2 = Subject.create(code='006209', name=None,
                         type_id=1, region_id=2, currency_code='NTD', is_fund=False)
    print('create_subjects end')


def create_transactions():
    acc = Account.get(id=1)
    sub = Subject.get(code='0050')
    Transaction.create(date=date(2019, 5, 16), type_id=1, account=acc, subject=sub,
                       price=79.5, amount=1, commission=32)
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
        NTD.format(hs.regions.value), USD.format(USD.from_ntd(hs.regions.value))))

    def format_type(v_sub):
        return "{}: {:.1%} ({:.0f})".format(v_sub.name, v_sub.ratio, v_sub.value / 10000)
    s_types = hs.types.sorted_children
    print(tuple(format_type(child) for child in s_types))
    print("  Fund:", tuple(format_type(child) for child in s_types[0].sorted_children))

    def format_region(v_sub):
        return "{}: {:.1%} ({:.0f})".format(v_sub.name, v_sub.ratio, v_sub.value / 10000)
    s_regions = hs.regions.sorted_children
    print(tuple(format_region(child) for child in s_regions))

    def format_currency(v_sub):
        currency = create_currency(v_sub.children[0].subject.currency_code)
        formatted_value_ = currency.format(currency.from_ntd(v_sub.value))
        return "{}: {:.1%} ({})".format(v_sub.name, v_sub.ratio, formatted_value_)
    s_currencies = hs.currencies.sorted_children
    print(tuple(format_currency(child) for child in s_currencies))


def print_holding_subjects():
    subs = [sub for sub in Subject.select() if sub.holding > 0.1]
    sorted_subs = sorted(iter(subs), key=lambda s: s.holding, reverse=True)

    def format_s(s):
        return repr((s.code,  "%.0f" % s.holding, "%.2f" % s.avg_cost))
    print("\n".join(format_s(s) for s in sorted_subs))


if __name__ == "__main__":
    # create_subjects()
    # create_transactions()
    # create_transactions_by_raws()
    print_foreign_balance()
    # print_holding_subjects()
    print_holding_value()
    print('end')
