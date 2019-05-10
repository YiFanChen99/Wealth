#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from Model.DataAccessor.ConfigureIntegrator.Loader import ConfigureLoader as ConLoader


class Path(object):
    DATA_DIR = os.getcwd() + os.sep + "Data"


class Configure(object):
    CONFIG = ConLoader.load_integrated_config(Path.DATA_DIR)
