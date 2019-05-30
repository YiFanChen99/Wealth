#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date
from PyQt5.QtWidgets import *

from Model.Constant import CONFIGURE  # init db
from PyQt.PyQtComponent.Table import ProxyTableView
from PyQt.TableModel.TransactionTableModel import TransactionProxyModel, TransactionRecordModel


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    so_m = TransactionRecordModel()
    px_m = TransactionProxyModel(cond_date=date(2019, 5, 15))
    widget = ProxyTableView(so_m, proxy_model=px_m)
    widget.show()
    app.exec_()
