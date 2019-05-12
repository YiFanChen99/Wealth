#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.DbRecordModel.BaseModel import BaseRecordModel
from Model.DataAccessor.DbTableAccessor import Subject, SubjectType, SubjectRegion
from Model.Currency import create_currency


class SubjectUtility(object):
    TYPE_MAP = {type.id: type for type in SubjectType.select()}
    REGION_MAP = {region.id: region for region in SubjectRegion.select()}

    @classmethod
    def get_type_record(cls, type_):
        if isinstance(type_, SubjectType):
            return type_
        elif isinstance(type_, int):
            return cls.TYPE_MAP[type_]
        else:
            raise TypeError

    @classmethod
    def get_region_record(cls, region):
        if isinstance(region, SubjectRegion):
            return region
        elif isinstance(region, int):
            return cls.REGION_MAP[region]
        else:
            raise TypeError


class SubjectModel(BaseRecordModel):
    ACCESSOR = Subject

    def _init_by_record(self, record):
        self.id = record.id
        self._init_by_args(iter((record.code, record.type, record.region, record.currency)))

    def _init_by_args(self, iterator):
        self.code = next(iterator)
        self.type = SubjectUtility.get_type_record(next(iterator))
        self.region = SubjectUtility.get_region_record(next(iterator))
        self.currency = create_currency(next(iterator))

    def _get_sync_kwargs(self):
        return {
            'code': self.code, 'type': self.type,
            'region': self.region, 'currency': self.currency.code
        }

    @classmethod
    def create_record(cls, code, type_, region, currency):
        rec = cls(code, type_, region, currency)
        rec.sync_to_db()
        return rec
