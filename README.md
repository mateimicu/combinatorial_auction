# Combinatorial Auction
Experimenting with algorithm that maximise the profit for Combinatorial Auction probme

### Reports

* [LP model and initial experiments](docs/01_report.pdf)
* [Research on other solutions](docs/02_report.pdf)
* [Final results](docs/03_report.pdf)


An auxiliary report will be done based on the results of the following experiments:
* [All result for 1 minute timeout](docs/03_report_1_min_results.md)
* [All result for 5 minute timeout](docs/03_report_5_min_results.md)

### DataSets

We have the test datasets that can be found [here](data/datasets), in total we hage 630 files with auction data.

A special dataset can be found [here](data/custom_dataset) that is a small subset of the all the datasets that contains some small and large instances, it is mainly used for fast iterations.

Raw data for our experiments can be found [here](data/results), informations about the experiments can be found in the above reports.

* [experiment_01](data/results/experiment_01.json) is a result of running out LP model with no timeout
* [1_minute_time_out_full_run_binary_operation](data/results/1_minute_time_out_full_run_binary_operation.json) is result of running our unproved LP model with 1 minute timeout
* [5_minute_time_out_full_run_binary_operation](data/results/5_minute_time_out_full_run_binary_operation.json) is result of running our unproved LP model with 5 minute timeout
* [GreedyAverageItemsPrice_full_run](data/results/GreedyAverageItemsPrice_full_run.json)
* [GreedyBigBet_full_run](data/results/GreedyBigBet_full_run.json)
* [GreedyNumberOfItems_full_run](data/results/GreedyNumberOfItems_full_run.json)
* [aoc_firs_implementation_5sec](data/results/aoc_firs_implementation_5sec.josn)
* [10_sec_groupe1_dataset_on_all_solutions_1_retry](data/results/10_sec_groupe1_dataset_on_all_solutions_1_retry) result of running all models one time over the groupe1 dataset with a 10 second timeout
* [aoc_second_5_seconds](data/results/aoc_second_5_seconds.json) result of running the improved ACO on all datasets
* [5_min_custom_datasets_all_retry_1](data/results/5_min_custom_datasets_all_retry_1) result of running on the custom dataset all solutions with a 5 minute timeout
* [parial_results](data/results/partial_results) this a partial runs that were termianted

### Sources
Every solution is based on this [base_model](src/base_solution.py).

We have a few solutions:

 * LP model that can be found [here](src/lp_model.py)
 * A few greedy implementation that can be found [here](src/greedy_model.py)
   * GreedyBigBet - is ordering bids by the amount they offer
   * GreedyNumberOfItems - is ordering bids by the amount if items the bid contains
   *  GreedyAverageItemsPrice - is ordering bids by the average price/item
 * Ant Colony Optimization that can be found [here](src/aoc_model.py) - this is the first solution, we can still improve it
 * Ant Colony Optimization that can be found [here](src/aoc_model.py) that uses 1000 ants to encourage exploration


A utility tool to generate Markdown with tables based on a summary, can be found [here](src/create_markdown_table_from_result.py).

Also a tool that compared results to one another can be found [here](src/plots.py), it is already liked to existing experiment results, you can run it and see how differing experiments compare with each other and offer static data on the results.

Team Members:

* Glodeanu  Irina-Elena
* Micu Matei-Marius
