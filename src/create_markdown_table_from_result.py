#!/usr/bin/env python
"""
Create a markdown Table from a summary file.
"""
import argparse
import os
import json


def get_parser():
    """Return a CLI parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('SOURCE', type=str,
                        help='JSON summary')

    parser.add_argument('DEST', type=str,
                        help='Destination of the markdown file')

    return parser


def main():
    """Main entry point."""
    parser = get_parser()
    args = parser.parse_args()

    data = json.loads(open(os.path.abspath(args.SOURCE), 'r').read())

    with open(args.DEST, 'w+') as fd:
        fd.writelines([
            '# Tabular data of the experiment \n',
            '\n',
            '\n',
            '|           Model Name           | Nr. Orders | Nr. Items  |   Profit   | Duration (seconds) |\n',
            '|--------------------------------|------------|------------|------------|--------------------|\n',
        ])
        for item in data['models']:
            # import pdb; pdb.set_trace()
            # try:
            time = float(item['delta_time'])
            # if time / 60 > 30:
            #     time = time / 60.0

            fd.write(
                '| {:30.30} | {:10.10} | {:10.10} | {:10.10} | {:18.2f} |\n'.format(
                    item['name'],
                    str(item['nr_orders']),
                    str(item['nr_items']),
                    float(item['profit']),
                    time,
                    ) 
            )
            # except Exception as exc:
                # import pdb; pdb.set_trace()

    print('Done ...')
if __name__ == '__main__':
    main()
