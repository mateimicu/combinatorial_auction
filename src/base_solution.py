#!/usr/bin/env python3

import time


class BaseSolution():
    def __init__(self, bids, name, logger):
        self._rez = None
        self._delta_time = 0
        self._bids = {}
        for index, data in enumerate(bids.items()):
            self._bids[index] = data
        self._name = name
        self._logger = logger

    def all_items(self):
        all_items = []
        for items, _ in self._bids.values():
            all_items += items
        return set(all_items)

    def get_profit(self):
        raise NotImplemented()

    def _get_status(self):
        return "NotSolved"

    def _extra_summary(self):
        pass

    def summary(self):
        self._extra_summary()
        self._logger.info("Total profit      => %s", self.get_profit())
        self._logger.info("Status            => %s", self._get_status())
        minutes = int(self._delta_time/ 60)
        seconds = int(self._delta_time% 60)
        self._logger.info(
            "Took              => %s minutes and %s  seconds", minutes, seconds)

    def _solve(self):
        raise NotImplemented()

    def solve(self, timeout=None):
        start_time = time.time()
        self._solve(timeout)
        delta_time = time.time() - start_time
        self._delta_time = delta_time
        return self._rez, self._delta_time


    def get_summary(self, file_path):
        return {
            "status": self._rez,
            "delta_time": self._delta_time,
            "nr_items": len(self.all_items()),
            "nr_orders": len(self._bids),
            "profit": self.get_profit(),
            "file_path": file_path,
            "name": self._name,
            "solver": self.__class__.__name__
        }

