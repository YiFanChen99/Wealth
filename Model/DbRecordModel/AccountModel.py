#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math  # for eval commission_rule

from Model.DbRecordModel.BaseModel import BaseRecordModel
from Model.DbRecordModel.Utility import TransactionSummarizer
from Model.DataAccessor.DbTableAccessor import Account
from Model.Currency import create_currency


class AccountModel(BaseRecordModel):
    ACCESSOR = Account

    def _init_by_record(self, record):
        self._init_by_args(iter((record.description, record.value, record.currency, record.commission_rule)))

    def _init_by_args(self, iterator):
        self.description = next(iterator)
        self.value = next(iterator)
        self.currency = create_currency(next(iterator))
        self._commission_rule_text = next(iterator)  # should be 'lambda...'
        self.commission_rule = eval(self._commission_rule_text)

    def _get_sync_kwargs(self):
        return {
            'description': self.description, 'value': self.value,
            'currency': self.currency.code, 'commission_rule': self._commission_rule_text
        }

    def deposit(self, amount):
        self.value += amount

    def withdraw(self, amount):
        self.value -= amount

    @property
    def transactions(self):
        if self.record is None:
            raise ValueError("Non-created Account.")
        return self.record.transactions

    @property
    def subjects(self):
        if self.record is None:
            raise ValueError("Non-created Account.")
        return self.record.subjects

    @property
    def balance(self):
        result = TransactionSummarizer(self.transactions)
        return self.value + result.income
