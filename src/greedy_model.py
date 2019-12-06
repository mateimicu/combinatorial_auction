#!/usr/bin/env python3
"""
Greedy solution to the winning determination problem.
"""

import os
import datetime
import time


import pulp

import base_solution



class GreedyBase(base_solution.BaseSolution):
    def __init__(self, bids, name, logger):
        super(GreedyBase, self).__init__(bids, name, logger)
        self._accepted_bids = []

    def _get_status(self):
        return "Solved"

    def get_profit(self):
        return sum([bid[1] for bid in self._accepted_bids])

    @staticmethod
    def _has_conflict(target_bid, accepted_bids):
        """Return true if the bid has items conflicts 
           with the currently accepted bids.
        """
        bid_items = set(target_bid[0])
        for bid in accepted_bids:
            if not bid_items.isdisjoint(set(bid[0])):
                return True
        return False


class GreedyNumberOfItems(GreedyBase):
    def __init__(self, bids, name, logger):
        super(GreedyNumberOfItems, self).__init__(bids, name, logger)

    def _solve(self, timeout=None):
        all_bids = list(self._bids.values())
        all_bids.sort(
            key=lambda x:len(x[0]),
            reverse=True)

        for bid in all_bids:
            if self._has_conflict(bid, self._accepted_bids):
                continue
            self._accepted_bids.append(bid)


class GreedyBigBet(GreedyBase):
    def __init__(self, bids, name, logger):
        super(GreedyBigBet, self).__init__(bids, name, logger)

    def _solve(self, timeout=None):
        all_bids = list(self._bids.values())
        all_bids.sort(
            key=lambda x: x[1],
            reverse=True)

        for bid in all_bids:
            if self._has_conflict(bid, self._accepted_bids):
                continue
            self._accepted_bids.append(bid)


class GreedyAverageItemsPrice(GreedyBase):
    def __init__(self, bids, name, logger):
        super(GreedyAverageItemsPrice, self).__init__(bids, name, logger)

    def _solve(self, timeout=None):
        all_bids = list(self._bids.values())

        # compute the average item price
        enhanced_bids = []
        for bid in all_bids:
            enhanced_bids.append(
                (bid, bid[1]/len(bid[0]))
            )
        enhanced_bids.sort(
            key=lambda x: x[1],
            reverse=True)

        # we don't care about average item price at this point
        for bid in [bid[0] for bid in enhanced_bids]:
            if self._has_conflict(bid, self._accepted_bids):
                continue
            self._accepted_bids.append(bid)
