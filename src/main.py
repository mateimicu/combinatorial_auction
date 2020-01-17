#!/usr/bin/env python3
import argparse
import os
import logging
import json

import base_solution
import lp_model
import greedy_model
import aoc_model
import aoc_model_second_generation


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


SOLUTIONS = [
    lp_model.LPModel,
    greedy_model.GreedyNumberOfItems,
    greedy_model.GreedyBigBet,
    greedy_model.GreedyAverageItemsPrice,
    aoc_model.AOCBaseSolution,
    aoc_model_second_generation.AOCBaseSolutionSecondGeneration,
]

ALL_SOLUTIONS = 'ALL'
SOLUTION_CHOICES = [sol.__name__ for sol in SOLUTIONS] + [ALL_SOLUTIONS]


def get_parser():
    parser = argparse.ArgumentParser(
            description='Tool for analyzing combinatorial auction solutions.')
    parser.add_argument('--summary-dir', default='summary_dir', type=str,
                        help='Directory for storing summary files.')
    parser.add_argument('-s', '--solutions',  type=str, required=True,
                        action='append', choices=SOLUTION_CHOICES)

    parser.add_argument('--datasets',  type=str, default='../data/datasets',
                        help='Location of the datasets.')

    parser.add_argument('--logging-lvl',  type=str, default='INFO',
                        choices=['INFO', 'DEBUG'],
                        help='Logging level.')

    parser.add_argument('-t', '--timeout',  type=int, default=None,
                        help='Nanoseconds to wait for a solution')

    parser.add_argument('-r', '--run-times',  type=int, default=1,
                        help='Times to run each solution.')

    return parser

def get_datasets(directory):
    # compute all data sources
    datasets = []
    for root, dirs, files in os.walk(os.path.abspath(directory), topdown=False):
        for name in files:
            file_path = os.path.join(os.path.abspath(root), name)
            size = os.stat(file_path).st_size
            datasets.append((name, file_path, size))

    datasets.sort(key=lambda x: x[2])
    return datasets

def save_summary(summary, summary_path):
    full_summary_path = os.path.abspath(summary_path)
    if not os.path.isfile(full_summary_path):
        with open(full_summary_path, "w+") as fd:
            fd.write('{}')

    with open(full_summary_path, "r+") as fp:
        data = json.load(fp)
    if "models" not in data:
        data["models"] = []

    data["models"].append(summary)
    with open(full_summary_path, "w") as fp:
        json.dump(data, fp)


def get_solutions(solution_names):
    """
    Return a list of solutions.
    """
    if len(solution_names) == 1 and solution_names[0] == ALL_SOLUTIONS:
        return SOLUTIONS

    solutions = []
    for sol in SOLUTIONS:
        if sol.__name__ in solution_names:
            solutions.append(sol)
    return solutions


def main():
    parser = get_parser()
    args = parser.parse_args()

    solutions = get_solutions(args.solutions)
    if not solutions:
        raise Exception("Can't find solver {}".format(args.solution))
    datasets = get_datasets(args.datasets)

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=args.logging_lvl,
        format='%(asctime)s %(message)s')

    summary_dir = os.path.abspath(args.summary_dir)
    if not os.path.exists(summary_dir):
        os.mkdir(summary_dir)

    if not os.path.isdir(summary_dir):
        raise Exception('{} is not a directory'.format(summary_dir))

    total_runs = len(datasets)*len(solutions)*args.run_times
    current_run = 0 

    for name, file_path, _ in datasets:
        logger.info('%s%s  %s  %s', '\n'*8, '-'*60, name, '-'*60)
        for solutionc_cls in solutions:
            file_name = '{}_summary.json'.format(solutionc_cls.__name__)
            output_file = os.path.join(summary_dir, file_name) 
            logger.info(
                '%s%s%s  %s  %s%s', '\n'*2, ' '*40,
                '+'*20, solutionc_cls.__name__, '+'*20, ' '*40)

            for itteration in range(args.run_times):
                current_run += 1
                logger.info("%s[%s][total_runs=%s/%s]Started work on %s ... %s",
                            '\n'*4, itteration, total_runs, current_run,
                            name, '\n'*4)
                bids = parse_file(file_path)
                logger.info("Creating model %s ...", name)
                auction_model = solutionc_cls(bids, "model_"+name, logger)
                logger.info("Solving %s ...", name)
                auction_model.solve(timeout=args.timeout)
                auction_model.summary()
                summary = auction_model.get_summary(file_path)
                summary['timeout'] = args.timeout
                save_summary(summary, output_file)


if __name__ == '__main__':
    main()
