#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict

from Model import DbRecordModel
from Model.Constant import CONFIGURE


class TransactionSummary(object):
    def __init__(self, transactions):
        self.income = 0
        self.net_amount = 0
        self.avg_price = 0
        self.commission = 0

        self.summarize(transactions)

    def summarize(self, transactions):
        if len(transactions) == 0:
            return
        elif not isinstance(transactions[0], DbRecordModel.TransactionModel.Transaction):
            raise TypeError

        for trans in transactions:
            self.commission += trans.commission

            if trans.type.name == '買':
                self.income -= trans.volume + trans.commission
                new_mount = self.net_amount + trans.amount
                self.avg_price = (self.volume + trans.volume) / new_mount
                self.net_amount = new_mount
            elif trans.type.name == '賣':
                self.income += trans.volume - trans.commission
                self.net_amount -= trans.amount
                if self.net_amount <= 0.1:
                    self.net_amount = 0  # floating error
                    self.avg_price = 0
            elif trans.type.name == '除息':
                self.income += trans.price - trans.commission
                self.avg_price -= trans.price / self.net_amount
            elif trans.type.name == '除權':
                new_mount = self.net_amount + trans.amount
                self.avg_price *= self.net_amount / new_mount
                self.net_amount += new_mount
            else:
                raise NotImplementedError

    @property
    def volume(self):
        return self.avg_price * self.net_amount


class HoldingValueSummary(object):
    @staticmethod
    def _sorted(dict_):
        return sorted(dict_.items(), key=lambda item: item[1], reverse=True)

    def __init__(self, subjects):
        self.total_value = 0
        self.types = defaultdict(lambda: 0)
        self.regions = defaultdict(lambda: 0)
        self.currencies = defaultdict(lambda: 0)

        self.summarize(subjects)

    def summarize(self, subjects):
        if len(subjects) == 0:
            return
        elif not isinstance(subjects[0], DbRecordModel.SubjectModel.Subject):
            raise TypeError

        for subject in subjects:
            if not subject.is_holding:
                continue

            ntd_value = subject.currency.to_ntd(
                subject.holding * CONFIGURE.CURRENT_PRICES[subject.code])
            self.total_value += ntd_value
            self.types[subject.type] += ntd_value
            self.regions[subject.region] += ntd_value
            self.currencies[subject.currency] += ntd_value

    @property
    def sorted_types(self):
        return tuple((type_, value / self.total_value) for type_, value in self._sorted(self.types))

    @property
    def sorted_regions(self):
        return tuple((region, value / self.total_value) for region, value in self._sorted(self.regions))

    @property
    def sorted_currencies(self):
        return tuple((currency, value / self.total_value, value) for currency, value in self._sorted(self.currencies))
