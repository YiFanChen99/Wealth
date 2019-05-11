#!/usr/bin/env python
# -*- coding: utf-8 -*-


def create_currency(code):
    if code == 'NTD' or code == 'TWD':
        return NTD()
    elif code == 'USD':
        return USD()
    else:
        raise ValueError


class Currency(object):
    SYMBOL = ''
    EXCHANGE_VALUE = 0

    def __init__(self, code=None):
        if not isinstance(code, str):
            raise TypeError

        self.code = code

    def str(self, amount):
        return "{} {}".format(self.SYMBOL, amount)

    def value(self, amount):
        return amount * self.EXCHANGE_VALUE


class NTD(Currency):
    SYMBOL = 'NT$'
    EXCHANGE_VALUE = 1

    def __init__(self):
        super().__init__(code='NTD')


class USD(Currency):
    SYMBOL = 'US$'
    EXCHANGE_VALUE = 30.9

    def __init__(self):
        super().__init__(code='USD')
