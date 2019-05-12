#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TransactionSummarizer(object):
    def __init__(self, transactions):
        self.income = 0
        self.net_amount = 0
        self.commission = 0

        self.summarizer(transactions)

    def summarizer(self, transactions):
        from Model.DbRecordModel.TransactionModel import Transaction

        if not isinstance(transactions[0], Transaction):
            raise TypeError

        for trans in transactions:
            if trans.type.name == '買':
                self.income -= trans.price * trans.amount + trans.commission
                self.net_amount += trans.amount
            elif trans.type.name == '賣':
                self.income += trans.price * trans.amount - trans.commission
                self.net_amount -= trans.amount
            elif trans.type.name == '除息':
                self.income += trans.price - trans.commission
            elif trans.type.name == '除權':
                self.net_amount += trans.amount - trans.commission
            else:
                raise NotImplementedError
            self.commission += trans.commission
