#!/usr/bin/env python3
"""
Greedy solution to the winning determination problem.
"""
import time
import copy

import numpy as np
import pandas as pd

import base_solution


class AOCBaseSolutionSecondGeneration(base_solution.BaseSolution):
    """Ant Colony Optimization solution."""

    def __init__(self, bids, name, logger,
                 ant_count=1000, pheromone_decay=0.9,
                 pheromone_power=0.5, greedy_power=0.5):
        super(AOCBaseSolutionSecondGeneration, self).__init__(
            bids, name, logger)
        self._accepted_bids = []
        self._ant_count = ant_count
        self._pheromone_decay = pheromone_decay
        self._pheromone_power = pheromone_power
        self._greedy_power = greedy_power
        self._status = 'NotStarted'

        # compute average item price for each bit
        all_bids = list(self._bids.values())
        self._enhanced_bids = []
        for bid in all_bids:
            self._enhanced_bids.append(
                (bid[0], bid[1], bid[1]/len(bid[0]))
            )
        self._enhanced_bids.sort(
            key=lambda x: x[2],
            reverse=True)

        # prepare ants
        self._ants = [[] for _ in range(self._ant_count)]
        self._pheromone_trail = [
            1 for _ in range(len(self._enhanced_bids))]

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

    def _get_status(self):
        return "Solved"

    def get_profit(self):
        return max([self._get_profit(ant) for ant in self._ants])

    @staticmethod
    def _get_profit(ant):
        return sum([bid[1] for bid in ant])

    def _solve(self, timeout=None):
        start_time = time.time()
        while time.time() - start_time <= timeout:
            progress = self.__next_epoch()
            self._status = 'PartiallyOptimized'
            if not progress:
                self._status = 'Finished'
                return

    def __next_epoch(self):
        # construct new solution
        index_of_chosen_bids = []
        added_item_to_ant = []
        for index_ant in range(len(self._ants)):
            # construct probability to add a bid
            valid_pheromon_array = []
            for index_bid, bid in enumerate(self._enhanced_bids):
                if self._has_conflict(bid, self._ants[index_ant]):
                    valid_pheromon_array.append(0.0)
                    continue
                valid_pheromon_array.append(self._pheromone_trail[index_bid])

            added_item_to_ant.append(any([x != 0.0 for x in valid_pheromon_array]))
            probability_array = []
            for index in range(len(self._enhanced_bids)):
                probability_array.append(
                    valid_pheromon_array[index]**self._pheromone_power + self._enhanced_bids[index][2]*self._greedy_power
                )
            total_power = sum(probability_array)
            probability_array = list(map(lambda x: x/total_power, probability_array))
            # import pdb; pdb.set_trace();
            winner_index_bid = np.random.choice(list(range(len(self._enhanced_bids))), p=probability_array)

            # add winning bid to ant
            self._ants[index_ant].append(self._enhanced_bids[winner_index_bid])
            index_of_chosen_bids.append(winner_index_bid)

        ant_fitness = [self._get_profit(ant) for ant in self._ants]
        max_ant_fitness = max([self._get_profit(ant) for ant in self._ants])
        index_of_max_fitness = ant_fitness.index(max_ant_fitness)
        bid_chosen = self._ants[index_of_max_fitness][-1]
        self._pheromone_trail[self._enhanced_bids.index(bid_chosen)] += max_ant_fitness

        # normalize trail
        self._pheromone_trail = [i/sum(self._pheromone_trail) for i in self._pheromone_trail]
        # TODO(mmicu):
        # - if you have time implement local search

        # evaporate pheromone trail
        for index in range(len(self._pheromone_trail)):
            self._pheromone_trail[index] = self._pheromone_trail[index]*(1-self._pheromone_decay)
        return any(added_item_to_ant)
