#!/usr/bin/env python3

import os
import datetime
import logging
import time


import pulp

import base_solution



class LPModel(base_solution.BaseSolution):
    def __init__(self, bids, name, logger):
        super(LPModel, self).__init__(bids, name, logger)
        self._vars = self._prepare_vars()
        self._model = self._prepare_model()

    def _prepare_vars(self):
        variables = pulp.LpVariable.dicts(
            'bid', list(self._bids.keys()),
            lowBound = 0,
            upBound = 1,
            cat = pulp.LpInteger)
        return variables

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

    def _save_model(self, model_name=None):
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

    def _get_status(self):
        return pulp.LpStatus[self._rez]

    def _extra_summary(self):
        self._logger.debug("Winning bids:")
        for index, data in self._bids.items():
            items, pay = data
            if self._vars[index].value() == 1.0:
                self._logger.debug("[{:5}]{:18} => {}".format(
                    str(index), str(items), pay))

    def _solve(self, timeout=None):
        start_time = time.time()
        # CPLEX will tell us that the problem in infeasible for large datasets
        # self._rez = self._model.solve(pulp.CPLEX())
        # import pdb; pdb.set_trace()
        options = ['--binarize']
        if timeout:
            options.extend(["--tmlim", str(timeout)])

        solver = pulp.GLPK(options=options)

        self._rez = self._model.solve(solver)
        delta_time = time.time() - start_time
        self._delta_time = delta_time
        return self._rez, self._delta_time
