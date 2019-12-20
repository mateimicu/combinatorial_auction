#!/usr/bin/env python3
import json

from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np



def get_data(path):
    with open(path, 'r') as fd:
        return json.loads(fd.read())



def main():
    lp_1_min = get_data('../data/results/1_minute_time_out_full_run_binary_operation.json')
    lp_5_min = get_data('../data/results/5_minute_time_out_full_run_binary_operation.json')
    gready_avg = get_data('../data/results/GreedyAverageItemsPrice_full_run.json')
    gready_items = get_data('../data/results/GreedyNumberOfItems_full_run.json')
    gready_bid = get_data('../data/results/GreedyBigBet_full_run.json')
    aoc_first_implementaion_5sec = get_data('../data/results/aoc_firs_implementation_5sec.josn')

    datasets = {
        'lp_1_min': lp_1_min,
        'lp_5_min': lp_5_min,
        'gready_avg': gready_avg,
        'gready_items': gready_items,
        'gready_bid': gready_bid,
        'aoc_first': aoc_first_implementaion_5sec,
    }

    data_array = np.arange(len(datasets))
    datapoints = []
    label = []
    for key, data in datasets.items():
        label.append(key)
        for model in data['models']:
            total_profit = 0
            # import pdb; pdb.set_trace()
            total_profit += model['profit']
        datapoints.append(total_profit)


    def millions(x, pos):
        'The two args are the value and tick position'
        return '{:.5}'.format(x)


    formatter = FuncFormatter(millions)

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(formatter)
    print(datapoints)
    plt.bar(data_array, datapoints)
    plt.xticks(data_array, label)
    plt.show()

if __name__ == '__main__':
    main()
