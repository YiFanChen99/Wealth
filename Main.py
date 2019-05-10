#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Model.DataAccessor.JsonAccessor.JsonAccessor import load_json
from Model.Constant import Configure


class Subject(object):
    @staticmethod
    def sum(subjects, getter=lambda s: s.volume()):
        return sum(getter(subject) for subject in subjects)

    @staticmethod
    def sum_by_group(subjects, group_id):
        groups = set((getattr(subject, group_id) for subject in subjects))

        subject_map = dict.fromkeys(groups, 0)
        for subject in subjects:
            group = getattr(subject, group_id)
            subject_map[group] += subject.volume()

        total = sum(subject_map.values())
        results = ((id, volume, volume / total) for id, volume in subject_map.items())
        return sorted(results, key=lambda t: t[1], reverse=True)

    def __init__(self, data):
        super().__init__()
        iterator = iter(data)
        self.id = next(iterator)
        self.desc = next(iterator)
        self.type = next(iterator)
        self.region = next(iterator)
        self.current_price = next(iterator)

        self.holding = 0
        self.cost = 0

    def trade(self, transactions):
        for price, shares in transactions:
            self.holding += shares
            self.cost += price * shares

    def volume(self, current_price=None):
        if current_price is None:
            current_price = self.current_price
        return self.holding * current_price


if __name__ == "__main__":
    data = load_json(Configure.CONFIG['json_path'])
    subjects = [Subject(subject) for subject in data['subject']]
    for id_, transactions in data['transaction'].items():
        subject = next(filter(lambda s: s.id == id_, subjects))
        subject.trade(transactions)

    type_res = Subject.sum_by_group(subjects, 'type')
    region_res = Subject.sum_by_group(subjects, 'region')

    print("Total: %.2f" % Subject.sum(subjects))
    print(["{0}: {1:2.2f}%".format(res[0], res[2]*100) for res in type_res])
    print(["{0}: {1:2.2f}%".format(res[0], res[2]*100) for res in region_res])
