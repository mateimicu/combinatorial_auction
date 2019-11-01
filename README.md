# Combinatorial Auction
Experimenting with algorithm that maximise the profit for Combinatorial Auction probme

### Reports

* [LP model and initial experiments](docs/01_report.pdf)
* [Research on other solutions](docs/02_report.md)


An auxiliary report will be done based on the results of the following experiments:
* [All result for 1 minute timeout](docs/03_report_1_min_results.md)
* [All result for 5 minute timeout](docs/03_report_5_min_results.md)

### DataSets

We have the test datasets that can be found [here](data/datasets), in total we hage 630 files with auction data.

Raw data for our experiments can be found [here](data/results), informations about the experiments can be found in the above reports.

* [experiment_01](data/results/experiment_01.json) is a result of running out LP model with no timeout
* [1_minute_time_out_full_run_binary_operation](data/results/1_minute_time_out_full_run_binary_operation.json) is result of running our unproved LP model with 1 minute timeout
* [5_minute_time_out_full_run_binary_operation](data/results/5_minute_time_out_full_run_binary_operation.json) is result of running our unproved LP model with 5 minute timeout

### Sources

We only have the LP model [here](src/lp_model.py). Future solutions will be based upon [base_model](src/base_solution.py).

A utility tool to generate Markdown with tables based on a summary, can be found [here](src/create_markdown_table_from_result.py).

Team Members:

* Glodeanu  Irina-Elena
* Micu Matei-Marius
