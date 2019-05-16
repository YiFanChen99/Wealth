#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        def sub_type_factory(parent, name):
            if name == 'NF':
                return ValuableSubjectGroup(parent, name)
            else:
                return ValuableGroupGroup(
                    parent, name, lambda subject: subject.type,
                    lambda parent_, name_: ValuableSubjectGroup(parent_, name_))
        self.types = ValuableGroupGroup(
            None, 'Type', lambda subject: 'Fund' if subject.is_fund else 'NF', sub_type_factory)
        self.regions = ValuableGroupGroup(
            None, 'Region', lambda subject: subject.region,
            lambda parent, name: ValuableSubjectGroup(parent, name))
        self.currencies = ValuableGroupGroup(
            None, 'Currency', lambda subject: subject.currency_code,
            lambda parent, name: ValuableSubjectGroup(parent, name))

        self.summarize(subjects)

    def summarize(self, subjects):
        for subject in subjects:
            self.types.push(subject)
            self.regions.push(subject)
            self.currencies.push(subject)


class Valuable(object):
    def __init__(self, parent, name):
        if (parent is not None) and (not isinstance(parent, Valuable)):
            raise TypeError

        super().__init__()
        self.parent = parent
        self.name = name
        self.value = 0  # Should be updated later

    @property
    def ratio(self):
        if self.parent is None:
            return 1
        else:
            return self.value / self.parent.value


class ValuableSubject(Valuable):
    def __init__(self, parent, subject):
        if not isinstance(subject, DbRecordModel.SubjectModel.Subject):
            raise TypeError

        super().__init__(parent, subject.code)
        self.subject = subject
        self.value = subject.currency.to_ntd(
            subject.holding * CONFIGURE.CURRENT_PRICES.get(subject.code, 0))


class ValuableSubjectGroup(Valuable):
    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.children = []

    def push(self, subject):
        child = ValuableSubject(self, subject)
        self.children.append(child)
        self.value += child.value
        return child

    @property
    def sorted_children(self):
        children = filter(lambda child: child.value > 0, self.children)
        return sorted(children, key=lambda child: child.value, reverse=True)


class ValuableGroupGroup(Valuable):
    def __init__(self, parent, name, key_getter, child_factory):
        if not callable(key_getter) or not callable(child_factory) :
            raise TypeError

        super().__init__(parent, name)
        self.children = {}
        self.child_factory = child_factory
        self.key_getter = key_getter

    def push(self, subject):
        key = self.key_getter(subject)
        try:
            child = self.children[key]
        except KeyError:
            child = self.child_factory(self, key)
            self.children[key] = child
        new_v_sub = child.push(subject)
        self.value += new_v_sub.value
        return new_v_sub

    @property
    def sorted_children(self):
        children = filter(lambda child: child.value > 0, self.children.values())
        return sorted(children, key=lambda child: child.value, reverse=True)
