#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from Model.DataAccessor.JsonAccessor.JsonAccessor import load_json
from Model.DataAccessor.ConfigureIntegrator.Loader import ConfigureLoader as ConLoader
from Model.DataAccessor.DbAccessor.DbOrmAccessor import db


class Path(object):
    DATA_DIR = os.getcwd() + os.sep + "Data"


class Configure(object):
    def __init__(self, db_path=None):
        self.CONFIG = ConLoader.load_integrated_config(Path.DATA_DIR)

        json_data = load_json(self.CONFIG['json_path'])
        self.EXCHANGE_RATES = json_data['exchange_rate']
        self.CURRENT_PRICES = json_data['current_price']

        if db_path is None:
            db_path = self.CONFIG['db_path']
        db.init(db_path)
        db.connect()


CONFIGURE = Configure()
