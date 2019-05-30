#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.DbRecordModel.TransactionModel import Transaction
from PyQt.PyQtComponent.Table import ProxyModel, ProxyModelCondition, BaseDbRecordTableModel


class TransactionProxyModel(ProxyModel):
        def __init__(self, cond_date=None, cond_account=None, cond_subject=None):
            pm_cond = ProxyModelCondition
            conditions = (
                pm_cond(key='date', value=cond_date,
                        comparator=lambda value, std: value > std),
                pm_cond(key='account', value=cond_account, hidden_column="Account"),
                pm_cond(key='subject', value=cond_subject, hidden_column="Subject"),
            )
            super().__init__(conditions)

        @property
        def cond_date(self):
            return self.get_condition_value('date')

        @cond_date.setter
        def cond_date(self, date_):
            self.update_condition_value('date', date_)

        @property
        def cond_account(self):
            return self.get_condition_value('account')

        @cond_account.setter
        def cond_account(self, account):
            self.update_condition_value('account', account)

        @property
        def cond_subject(self):
            return self.get_condition_value('subject')

        @cond_subject.setter
        def cond_subject(self, subject):
            self.update_condition_value('subject', subject)


class TransactionRecordModel(BaseDbRecordTableModel):
    MODEL = Transaction

    @classmethod
    def get_column_headers(cls, *args):
        return (
            ("Date", lambda tr: tr.date.strftime("%y-%m-%d")),
            ("Type", lambda tr: tr.type.name),
            ("Account", lambda tr: tr.account.description),
            ("Subject", lambda tr: tr.subject.code),
            ("Price", lambda tr: tr.price),
            ("Amount", lambda tr: tr.amount),
            ("Commission", lambda tr: tr.commission),
            ("Net", lambda tr: tr.balance_changed),
        )

    @classmethod
    def get_model_data(cls, *args):
        return tuple(cls.MODEL.select())

    def get_cell_data(self, q_index):
        getter = self.column_headers[q_index.column()][1]
        return getter(self.model_data[q_index.row()])
