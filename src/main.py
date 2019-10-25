#!/usr/bin/env python3

import os
import datetime
import logging
import time
import json

LOGGING = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

import pulp


BIDS = {
    ('b', 'c'): 5,
    ('a', 'b', 'c'): 12,
    ('a', 'c'): 8,
    ('a', ): 8,
    ('x', 'c'): 8,
    ('x', ): 8,
}

def parse_file(file_path):
    """Parse a file in the appropriate format for the model."""
    bids = {}
    with open(file_path, "r") as fd:
        # skip the first line with the number of items and
        # number of bids
        first_line = fd.readline()
        if first_line.endswith("#"):
            # index on line 
            for line in fd:
                money, *items = line.replace("#", "")[1:].trimp().split()
                bids[tuple(items)] = float(money)
        else:
            # no index on the line
            for line in fd:
                money, *items = line.split()
                bids[tuple(items)] = float(money)

    return bids

class Model():
    def __init__(self, bids, name, logger):
        self._rez = None
        self._delta_time = 0
        self._bids = {}
        for index, data in enumerate(bids.items()):
            self._bids[index] = data
        self._name = name
        self._logger = logger
        self._vars = self._prepare_vars()
        self._model = self._prepare_model()

    def _prepare_vars(self):
        variables = pulp.LpVariable.dicts(
            'bid', list(self._bids.keys()),
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger)
        return variables

    def all_items(self):
        all_items = []
        for items, _ in self._bids.values():
            all_items += items
        return set(all_items)

    def _prepare_model(self):

        model = pulp.LpProblem(
            "Auction Model "+self._name,
            pulp.LpMaximize)

        # maximize the profit
        model += pulp.lpSum(
            [self._bids[index][1] * self._vars[index] for index in self._vars])

        # Add restriction that you can only take
        # one bid if they share at least one item
        for item in self.all_items():
            restrictie = sum(
                [self._vars[index] for (index, data) in self._bids.items()
                                if item in data[0]]) <= 1, "max_one_pick_%s"%str(item)
            model  += restrictie
        return model

    def save_model(self, model_name=None):
        if model_name is None:
            model_name = "model_{}".format(datetime.datetime.now())
        self._logger.debug(self._model)


        self._logger.info("Saving the model as %s", model_name)
        self._model.writeLP(os.path.join("models", model_name+".lp"))
        self._model.writeMPS(os.path.join("models", model_name+".mps"))

    def get_profit(self):
        total_profit = 0
        for index, data in self._bids.items():
            _, pay = data
            if self._vars[index].value() == 1.0:
                total_profit += pay
        return total_profit


    def summary(self):
        self._logger.debug("Winning bids:")
        for index, data in self._bids.items():
            items, pay = data
            if self._vars[index].value() == 1.0:
                self._logger.debug("[{:5}]{:18} => {}".format(
                    str(index), str(items), pay))
        self._logger.info("Total profit      => %s", self.get_profit())
        self._logger.info("Status            => %s", pulp.LpStatus[self._rez])
        minutes = int(self._delta_time/ 60)
        seconds = int(self._delta_time% 60)
        self._logger.info(
            "Took              => %s minutes and %s  seconds", minutes, seconds)

    def solve(self):
        start_time = time.time()
        # CPLEX will tell us that the problem in infeasible for large datasets
        # self._rez = self._model.solve(pulp.CPLEX())
        self._rez = self._model.solve(pulp.GLPK())
        delta_time = time.time() - start_time
        self._delta_time = delta_time
        return self._rez, self._delta_time

    def save_summary(self, file_path):
        model_data = {
            "status": self._rez,
            "delta_time": self._delta_time,
            "nr_items": len(self.all_items()),
            "nr_orders": len(self._bids),
            "profit": self.get_profit(),
            "file_path": file_path,
            "name": self._name
        }

        with open("summary_data.json", "r+") as fp:
            data = json.load(fp)
        if "models" not in data:
            data["models"] = []

        data["models"].append(model_data)
        with open("summary_data.json", "w") as fp:
            json.dump(data, fp)


# compute all data sources
DATASOURCES = []
for root, dirs, files in os.walk(os.path.abspath("./data"), topdown=False):
    for name in files:
        file_path = os.path.join(os.path.abspath(root), name)
        size = os.stat(file_path).st_size
        DATASOURCES.append((name, file_path, size))

DATASOURCES.sort(key=lambda x: x[2])

for name, file_path, _ in DATASOURCES:
    LOGGING.info("Started work on %s ...", name)
    bids = parse_file(file_path)
    LOGGING.info("Creating model %s ...", name)
    auction_model = Model(bids, "model_"+name, LOGGING)
    auction_model.save_model()
    LOGGING.info("Solving %s ...", name)
    import pdb; pdb.set_trace()
    auction_model.solve()
    auction_model.summary()
    auction_model.save_summary(file_path)



# BIDS =  parse_file("/home/mmicu/Desktop/auction_problem/data/CAST_test_instance/arbitrary_40.txt")

# auction_model = Model(BIDS, "test_model", LOGGING)
# auction_model.solve()
# auction_model.summary()
