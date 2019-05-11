#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math  # for eval commission_rule

from Model.DbRecordModel.BaseModel import BaseRecordModel
from Model.DataAccessor.DbTableAccessor import Account
from Model.Currency import create_currency


class AccountModel(BaseRecordModel):
    ACCESSOR = Account

    def _init_by_record(self, record):
        self.id = record.id
        self._init_by_args(iter((record.description, record.balance, record.currency, record.commission_rule)))

    def _init_by_args(self, iterator):
        self.description = next(iterator)
        self.balance = next(iterator)
        self.currency = create_currency(next(iterator))
        self._commission_rule_text = next(iterator)  # should be 'lambda...'
        self.commission_rule = eval(self._commission_rule_text)

    def _get_sync_kwargs(self):
        return {
            'description': self.description, 'balance': self.balance,
            'currency': self.currency.code, 'commission_rule': self._commission_rule_text
        }

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
