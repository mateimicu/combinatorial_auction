#!/usr/bin/env python3
import os
import json
from statistics import median, mean

from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np

import base_solution
import lp_model
import greedy_model
import aoc_model
import aoc_model_second_generation

SOLUTIONS = [
    lp_model.LPModel,
    greedy_model.GreedyNumberOfItems,
    greedy_model.GreedyBigBet,
    greedy_model.GreedyAverageItemsPrice,
    aoc_model.AOCBaseSolution,
    aoc_model_second_generation.AOCBaseSolutionSecondGeneration,
]

SOLUTIONS_TO_SHORT_NAMES = {
    lp_model.LPModel.__name__: 'lp',
    greedy_model.GreedyNumberOfItems.__name__: 'g_items',
    greedy_model.GreedyBigBet.__name__: 'g_big',
    greedy_model.GreedyAverageItemsPrice.__name__: 'g_avg',
    aoc_model.AOCBaseSolution.__name__: 'aco',
    aoc_model_second_generation.AOCBaseSolutionSecondGeneration.__name__: 'aco_s',
}


def autolabel(rects, axes, convert=True):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        text = '%.1f' % float(height)
        if convert:
            text = '%dK' % (int(height) / 1000)
        axes.text(
            rect.get_x() + rect.get_width()/2., 1.05*height,
            text, ha='center', va='bottom')


def get_data(path):
    with open(path, 'r') as fd:
        return json.loads(fd.read())


def get_directory_data(directory_path):
    models = []
    # for file_name in os.listdir(directory_path):
    #     file_path = os.path.join(directory_path, file_name)
    #     if not os.path.isfile(file_path):
    #         continue


    for root, dirs, files in os.walk(os.path.abspath(directory_path), topdown=False):
        for name in files:
            if name == '.DS_Store':
                continue
            file_path = os.path.join(os.path.abspath(root), name)
            data = get_data(file_path)
            models += data['models']

    return models


def main():
    # histogram price
    lp_1_min = get_data('../data/results/1_minute_time_out_full_run_binary_operation.json')
    lp_5_min = get_data('../data/results/5_minute_time_out_full_run_binary_operation.json')
    gready_avg = get_data('../data/results/GreedyAverageItemsPrice_full_run.json')
    gready_items = get_data('../data/results/GreedyNumberOfItems_full_run.json')
    gready_bid = get_data('../data/results/GreedyBigBet_full_run.json')
    aoc_first_implementaion_5sec = get_data('../data/results/aoc_firs_implementation_5sec.josn')
    aoc_second_implementaion_5sec = get_data('../data/results/aoc_second_5_seconds.json')

    datasets = {
        'lp_1m': lp_1_min,
        'lp_5m': lp_5_min,
        'g_avg': gready_avg,
        'g_items': gready_items,
        'g_bid': gready_bid,
        'aco': aoc_first_implementaion_5sec,
        'aco_s': aoc_second_implementaion_5sec
    }

    data_array = np.arange(len(datasets))
    datapoints = []
    label = []
    for key, data in datasets.items():
        label.append(key)
        total_profit = 0
        for model in data['models']:
            total_profit += model['profit']
        datapoints.append(total_profit)

    t_data_array = np.arange(len(datasets))
    t_datapoints = []
    for key, data in datasets.items():
        total_time = 0
        for model in data['models']:
            total_time += model['delta_time']
        t_datapoints.append(total_time)

    grid = plt.GridSpec(4, 4, wspace=0.4, hspace=0.3, top=0.92, left=0.03, right=0.97, bottom=0.05)

    axes = plt.subplot(grid[0, 0:2])
    plt.gca().set_title('Total price(full)', pad=20)
    rect = plt.bar(data_array, datapoints)
    axes.set_xticklabels([None] + label)
    autolabel(rect, axes)

    axes = plt.subplot(grid[0, 2:])
    plt.gca().set_title('Histogram compute time', pad=20)
    rect = plt.bar(t_data_array, t_datapoints)
    axes.set_xticklabels([None] + label)
    autolabel(rect, axes, False)

    # get all summary for a specific type
    models = get_directory_data('../data/results/5_min_custom_datasets_all_retry_1')
    # models = get_directory_data('../data/results/10_sec_groupe1_dataset_on_all_solutions_1_retry')
    # models = get_directory_data('1_min_groupe1_dataset_on_all_solutions_5_retry/')
    # models = get_directory_data('10_sec_groupe1_dataset_on_all_solutions_1_retry')
    # models = get_directory_data('5_min_custom_datasets_all_retry_1')
    split_models = {sol.__name__: [] for sol in SOLUTIONS}

    # import pdb; pdb.set_trace()
    for model in models:
        if 'solver' not in model:
            continue
        if model['solver'] not in split_models:
            split_models[model['solver']] = []
        split_models[model['solver']].append(model)

    # plot dataset

    axes = plt.subplot(grid[3, 3])
    plt.gca().set_title('Sample dataset distribution')
    plt.plot(
        [model['nr_items'] for model in models],
        [model['nr_orders'] for model in models],
        '+'
        )
    plt.xlabel('nr_items')
    plt.ylabel('nr_orders')

    # mean price and median price
    width = 0.35
    labels = []
    mean_data = []
    median_data = []
    for model_name, models in split_models.items():
        labels.append(model_name)
        mean_data.append(mean([model['profit'] for model in models]))
        median_data.append(median([model['profit'] for model in models]))
    x = np.arange(len(labels))


    axes = plt.subplot(grid[1, 0:2])
    plt.gca().set_title('Mean and median')
    rect1 = plt.bar(x - width/2, mean_data, width, label='mean')
    rect2 = plt.bar(x + width/2, median_data, width, label='median')
    axes.set_xticklabels([None] + [SOLUTIONS_TO_SHORT_NAMES[l] for l in labels])
    plt.legend()
    autolabel(rect1, axes)
    autolabel(rect2, axes)

    # min and max
    width = 0.35
    labels = []
    min_data = []
    max_data= []
    for model_name, models in split_models.items():
        labels.append(model_name)
        min_data.append(min([model['profit'] for model in models])) 
        max_data.append(max([model['profit'] for model in models])) 
    x = np.arange(len(labels)) 


    axes = plt.subplot(grid[2, 0:2])
    plt.gca().set_title('Min and Max')
    rect1 = plt.bar(x - width/2, min_data, width, label='min')
    rect2 = plt.bar(x + width/2, max_data, width, label='max')
    axes.set_xticklabels([None] + [SOLUTIONS_TO_SHORT_NAMES[l] for l in labels])
    plt.legend()
    autolabel(rect1, axes)
    autolabel(rect2, axes)

    # total_profit_for_sample dataset
    width = 0.35
    labels = []
    total_profit_data = []
    for model_name, models in split_models.items():
        labels.append(model_name)
        total_profit_data.append(sum([model['profit'] for model in models]))
    x = np.arange(len(labels))

    axes = plt.subplot(grid[2, 2:])

    plt.gca().set_title('Total Profit on sample')
    rect = plt.bar(x, total_profit_data, width, label='total_profit')
    axes.set_xticklabels([None] + [SOLUTIONS_TO_SHORT_NAMES[l] for l in labels])
    plt.legend()
    autolabel(rect, axes)

    # percentile runtime
    width = 0.35
    labels = []
    percentile_99 = []
    percentile_95 = []
    percentile_90 = []
    percentile_80 = []
    for model_name, models in split_models.items():
        labels.append(model_name)
        percentile_99.append(
            np.percentile([model['delta_time'] for model in models], 90))
        percentile_95.append(
            np.percentile([model['delta_time'] for model in models], 95))
        percentile_90.append(
            np.percentile([model['delta_time'] for model in models], 90))
        percentile_80.append(
            np.percentile([model['delta_time'] for model in models], 80))
    x = np.arange(len(labels))

    axes = plt.subplot(grid[3, 0:3])
    width = 0.65
    plt.gca().set_title('Runtime percentile')
    rect1 = plt.bar(x - 2*width/4, percentile_99, width/4, label='p99')
    rect2 = plt.bar(x - 1*width/4, percentile_95, width/4, label='p95')
    rect3 = plt.bar(x , percentile_90, width/4, label='p90')
    rect4 = plt.bar(x + 1*width/4, percentile_80, width/4, label='p80')
    axes.set_xticklabels([None] + [SOLUTIONS_TO_SHORT_NAMES[l] for l in labels])
    plt.legend()
    autolabel(rect1, axes, False)
    autolabel(rect2, axes, False)
    autolabel(rect3, axes, False)
    autolabel(rect4, axes, False)

    # Total compute time
    compute_time = []
    labels = []
    for model_name, models in split_models.items():
        labels.append(model_name)
        compute_time.append(sum([model['delta_time'] for model in models]))

    axes = plt.subplot(grid[1, 2:])
    plt.gca().set_title('Histogram compute time (sample)', pad=20)
    rect = plt.bar(x, compute_time)
    axes.set_xticklabels([None] + [SOLUTIONS_TO_SHORT_NAMES[l] for l in labels])
    autolabel(rect, axes, False)

    plt.show()


if __name__ == '__main__':
    main()
