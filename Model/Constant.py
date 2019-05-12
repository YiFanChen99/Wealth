#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from Model.DataAccessor.ConfigureIntegrator.Loader import ConfigureLoader as ConLoader
from Model.DataAccessor.DbAccessor.DbOrmAccessor import db
from Model.DataAccessor.DbTableAccessor import SubjectType, SubjectRegion, TransactionType
from Model.DbRecordModel.BaseModel import SimpleModelMap


class Path(object):
    DATA_DIR = os.getcwd() + os.sep + "Data"


class Configure(object):
    def __init__(self, db_path=None):
        self.CONFIG = ConLoader.load_integrated_config(Path.DATA_DIR)

        if db_path is None:
            db_path = self.CONFIG['db_path']
        db.init(db_path)
        db.connect()


CONFIGURE = Configure()
