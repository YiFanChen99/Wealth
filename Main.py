#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date

from Model.Constant import CONFIGURE  # init db
from Model.DbRecordModel.AccountModel import Account
from Model.DbRecordModel.SubjectModel import Subject, TYPE_MAP as S_TYPE_MAP, REGION_MAP
from Model.DbRecordModel.TransactionModel import Transaction, TYPE_MAP as T_TYPE_MAP

'''
class Subject(object):
    @staticmethod
    def sum(subjects, getter=lambda s: s.volume()):
        return sum(getter(subject) for subject in subjects)

    @staticmethod
    def sum_by_group(subjects, group_id):
        groups = set((getattr(subject, group_id) for subject in subjects))

        subject_map = dict.fromkeys(groups, 0)
        for subject in subjects:
            group = getattr(subject, group_id)
            subject_map[group] += subject.volume()

        total = sum(subject_map.values())
        results = ((id, volume, volume / total) for id, volume in subject_map.items())
        return sorted(results, key=lambda t: t[1], reverse=True)

    def __init__(self, data):
        super().__init__()
        iterator = iter(data)
        self.id = next(iterator)
        self.desc = next(iterator)
        self.type = next(iterator)
        self.region = next(iterator)
        self.currency_ratio = exchange_currency(next(iterator))
        self.current_price = next(iterator)

        self.holding = 0
        self.cost = 0

    def trade(self, transactions):
        for price, shares in transactions:
            self.holding += shares
            self.cost += price * shares

    def volume(self, current_price=None):
        if current_price is None:
            current_price = self.current_price
        return self.holding * current_price * self.currency_ratio


def main1():
    data = load_json(CONFIGURE.CONFIG['json_path'])
    subjects = [Subject(subject) for subject in data['subject']]
    for id_, transactions in data['transaction'].items():
        subject = next(filter(lambda s: s.id == id_, subjects))
        subject.trade(transactions)

    type_res = Subject.sum_by_group(subjects, 'type')
    region_res = Subject.sum_by_group(subjects, 'region')

    print("Total: NTD %.2f*10K (USD %.2f*K)"
          % (Subject.sum(subjects) / 10000, Subject.sum(subjects) / exchange_currency("USD") / 1000))
    print(["{0}: {1:2.2f}%".format(res[0], res[2]*100) for res in type_res])
    print(["{0}: {1:2.2f}%".format(res[0], res[2]*100) for res in region_res])
'''


def create_subjects():
    print('type:', S_TYPE_MAP)
    print('region:', REGION_MAP)
    sm2 = Subject.create(code='006209', type_id=1, region_id=2, currency_code='NTD')
    print('create_subjects end')


def create_transactions():
    print('type:', T_TYPE_MAP)
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


def main2():
    # create_transactions_by_raws()

    sk = Account.get(id=1)
    sk_balance = sk.balance

    sk_tr = sk.transactions
    sk_subjs = sk.subjects
    sk_amount_list = [(sub.code, sub.holding) for sub in sk_subjs]

    ft = Account.get(id=2)
    ft_balance = ft.balance

    first_tr = ft.transactions
    ft_subjs = ft.subjects
    ft_amount_list = [(sub.code, sub.holding) for sub in ft_subjs]
    print('end')


if __name__ == "__main__":
    main2()
