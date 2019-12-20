#!/usr/bin/env python3
import argparse
import os
import logging
import json

import base_solution
import lp_model
import greedy_model
import aoc_model


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
]

def get_parser():
    parser = argparse.ArgumentParser(
            description='Tool for analyzing combinatorial auction solutions.')
    parser.add_argument('--summary-file', default='summary.json', type=str,
                        help='File that will contain results of the runs in json format')
    parser.add_argument('-s', '--solution',  type=str, required=True,
                        choices=[sol.__name__ for sol in SOLUTIONS])

    parser.add_argument('--datasets',  type=str, default='../data/datasets',
                        help='Location of the datasets.')

    parser.add_argument('--logging-lvl',  type=str, default='INFO',
                        choices=['INFO', 'DEBUG'],
                        help='Logging level.')

    parser.add_argument('-t', '--timeout',  type=int, default=None,
                        help='Nanoseconds to wait for a solution')

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


def main():
    parser = get_parser()
    args = parser.parse_args()

    solution = None 
    for sol in SOLUTIONS:
        if sol.__name__ == args.solution:
            solution = sol
            break
    if solution is None:
        raise Exception("Can't find solver {}".format(args.solution))

    datasets = get_datasets(args.datasets)

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=args.logging_lvl,
        format='%(asctime)s %(message)s')

    for name, file_path, _ in datasets:
        logger.info('%s%s  %s  %s', '\n'*8, '-'*60, name, '-'*60)
        logger.info("Started work on %s ...", name)
        bids = parse_file(file_path)
        logger.info("Creating model %s ...", name)
        auction_model = solution(bids, "model_"+name, logger)
        # auction_model.save_model()
        logger.info("Solving %s ...", name)
        auction_model.solve(timeout=args.timeout)
        auction_model.summary()
        summary = auction_model.get_summary(file_path)
        summary['timeout'] = args.timeout
        save_summary(summary, args.summary_file)


if __name__ == '__main__':
    main()
