#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.Constant import CONFIGURE


def create_currency(code):
    if code == 'NTD' or code == 'TWD':
        return NTD()
    elif code == 'USD':
        return USD()
    else:
        raise ValueError


class Currency(object):
    SYMBOL = '$'
    EXCHANGE_RATE = 0

    def __init__(self, code=None):
        if not isinstance(code, str):
            raise TypeError

        self.code = code

    def __repr__(self):
        return repr(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash(self.code)

    @classmethod
    def format(cls, amount):
        raise NotImplementedError

    @classmethod
    def to_ntd(cls, amount):
        return amount * cls.EXCHANGE_RATE

    @classmethod
    def from_ntd(cls, amount):
        return amount / cls.EXCHANGE_RATE


class NTD(Currency):
    SYMBOL = 'NT $'
    EXCHANGE_RATE = 1

    def __init__(self):
        super().__init__(code='NTD')

    @classmethod
    def format(cls, amount):
        return "{}{:.1f}萬".format(cls.SYMBOL, amount / 10000)


class USD(Currency):
    SYMBOL = 'US $'
    EXCHANGE_RATE = CONFIGURE.EXCHANGE_RATES['USD']

    def __init__(self):
        super().__init__(code='USD')

    @classmethod
    def format(cls, amount):
        return "{}{:.1f}k".format(cls.SYMBOL, amount / 1000)
