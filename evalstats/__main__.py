#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import argparse
import platform
from time import time as now
from evalstats import EvalStats
from evalstats import __version__

__author__ = ['Nico Curti']
__email__ = ['nico.curti2@unibo.it']

RESET_COLOR_CODE  = '\033[0m'
GREEN_COLOR_CODE  = '\033[38;5;40m'
ORANGE_COLOR_CODE = '\033[38;5;208m'
VIOLET_COLOR_CODE = '\033[38;5;141m'
RED_COLOR_CODE    = '\033[38;5;196m'
CRLF              = '\r\x1B[K' if platform.system() != 'Windows' else '\r\x1b[2K'

def parse_args():
  '''
  Parse command line arguments for the evalstats package.
  This function sets up the argument parser, defines the expected arguments,
  and returns the parsed arguments.

  Returns
  -------
  argparse.Namespace
    The parsed command line arguments as a Namespace object.

  Raises
  -------
  argparse.ArgumentError
    If there is an error in the argument parsing, such as a missing required
    argument or an invalid value.
  '''
  # global sofware information
  parser = argparse.ArgumentParser(
    prog='evalstats',
    argument_default=None,
    add_help=True,
    prefix_chars='-',
    allow_abbrev=True,
    exit_on_error=True,
    description='Evaluate the main statistics of a given set of data.',
  )

  # evalstats <data>
  # This positional argument allows the user to provide the input data for 
  # which statistics will be computed.
  # It should be a list of numbers separated by spaces.
  # If the user provides this argument, it will take precedence over the
  # --input option. The data will be converted to a list of floats.
  parser.add_argument(
    '--data', '-d',
    type=str,
    nargs='+',
    required=False,
    default=None,
    help=(
      'The input data for which statistics will be computed. '
      'It should be a list of numbers separated by spaces. '
      'If not provided, an input file must be specified using --input.'
      ' Example: --data 1.0 2.5 3.6 4.2'
    ),
  )

  # evalstats --input <file>
  # This option allows the user to specify an input file from which to read the data.
  # If both 'data' and 'input' are provided, 'data' will take precedence.
  parser.add_argument(
    '--input', '-i',
    dest='input',
    type=str,
    required=False,
    default=None,
    help=(
      'The input file from which to read the data. '
      'If not provided, data must be passed as a positional argument.'
    ),
  )
  
  # evalstats --num-workers <int>
  # This option allows the user to specify the number of worker threads 
  # to use for parallel computation.
  parser.add_argument(
    '--num-workers', '-n',
    dest='num_workers',
    type=int,
    required=False,
    default=4,
    help='The number of worker threads to use for parallel computation. Default is 4.',
  )

  # evalstats --mean
  # This option allows the user to compute the mean of the data.
  parser.add_argument(
    '--mean', '-mu',
    dest='mean',
    action='store_true',
    default=False,
    help='Compute the mean of the data.',
  )

  # evalstats --std
  # This option allows the user to compute the standard deviation of the data.
  parser.add_argument(
    '--std', '-S',
    dest='std',
    action='store_true',
    default=False,
    help='Compute the standard deviation of the data.',
  )

  # evalstats --min
  # This option allows the user to compute the minimum value of the data.
  parser.add_argument(
    '--min', '-m',
    dest='min',
    action='store_true',
    default=False,
    help='Compute the minimum value of the data.',
  )

  # evalstats --max
  # This option allows the user to compute the maximum value of the data.
  parser.add_argument(
    '--max', '-M',
    dest='max',
    action='store_true',
    default=False,
    help='Compute the maximum value of the data.',
  )

  # evalstats --count
  # This option allows the user to count the number of elements in the data.
  parser.add_argument(
    '--count', '-c',
    dest='count',
    action='store_true',
    default=False,
    help='Count the number of elements in the data.',
  )

  # evalstats --sum
  # This option allows the user to compute the sum of the data.
  parser.add_argument(
    '--sum', '-s',
    dest='sum',
    action='store_true',
    default=False,
    help='Compute the sum of the data.',
  )

  # evalstats --variance
  # This option allows the user to compute the variance of the data.
  parser.add_argument(
    '--variance', '-V',
    dest='variance',
    action='store_true',
    default=False,
    help='Compute the variance of the data.',
  )

  # evalstats --all
  # This option allows the user to compute all statistics at once.
  parser.add_argument(
    '--all', '-A',
    dest='all',
    action='store_true',
    default=False,
    help='Compute all statistics (mean, std, min, max, count, sum, variance).',
  )

  # evalstats --output <file>
  parser.add_argument(
    '--output', '-o',
    dest='output',
    type=str,
    required=False,
    default=None,
    help=(
      'The output file to save the computed statistics. '
      'If not provided, results will be printed to stdout.'
    ),
  )

  # evalstats --version
  parser.add_argument(
    '--version', '-v',
    dest='version',
    required=False,
    action='store_true',
    default=False,
    help='Get the current version installed',
  )

  return parser

def main ():
  # extract the arguments of the cmd
  parser = parse_args()
  args = parser.parse_args()
  
  # source: https://patorjk.com/software/taag
  print(fr'''{VIOLET_COLOR_CODE}
                 _     _        _       
  _____   ____ _| |___| |_ __ _| |_ ___ 
 / _ \ \ / / _` | / __| __/ _` | __/ __|
|  __/\ V / (_| | \__ \ || (_| | |_\__ \
 \___| \_/ \__,_|_|___/\__\__,_|\__|___/
                                        
    {RESET_COLOR_CODE}''',
    file=sys.stdout, flush=True
  )
  

  # start the timer
  tic = now()

  if args.version:
    print(__version__, file=sys.stdout, flush=True)
    exit(0)

  # create a data array if the user provided it
  data = args.data    

  # check if the user wants to use an in
  # input file or a data array
  if data is None and args.input is None:
    print(
      f'{RED_COLOR_CODE}Error! You must provide either data or an input file.{RESET_COLOR_CODE}', 
      file=sys.stderr, flush=True
    )
    print(parser.print_help(), file=sys.stdout, flush=True)    
    exit(1)
  # check if both data and input file are provided
  # and use the data array if both are present
  elif data is not None:
    # convert the data array to a list of floats
    data = [
      float(x) 
      for x in data
    ]
    if args.input is not None:
      # if both data and input file are provided,
      # we will use the data array and print a warning
      # message to the user
      print(
        f'{ORANGE_COLOR_CODE}Warning! Both data and input file provided. Using data array.{RESET_COLOR_CODE}',
        file=sys.stdout, flush=True
      )
    else:
      # if only data is provided, we will use it
      print(
        f'{ORANGE_COLOR_CODE}Using provided data array{RESET_COLOR_CODE}',
        file=sys.stdout, flush=True
      )
  # check if the user wants to use an input file
  elif args.input is not None:
    # check if the input file exists and can be opened
    if not args.input.endswith('.csv'):      
      print(
        f'{RED_COLOR_CODE}Error! Input file must be a CSV file.{RESET_COLOR_CODE}',
        file=sys.stderr, flush=True
      )
      exit(1)
    # try to open the input file to check if it exists
    try:
      # read the input file
      with open(args.input, 'r') as fp:
        # read the data from the file
        # split the lines 
        data = fp.read().splitlines()

      # convert the data to a list of floats
      data = [
        [
          float(x) 
          for x in row.strip().split(',')
        ] 
        for row in data
      ]
    except FileNotFoundError:
      print(
        f'{RED_COLOR_CODE}Error! Input file {args.input} not found.{RESET_COLOR_CODE}',
        file=sys.stderr, flush=True
      )
      exit(1)
    
    print(
      f'{ORANGE_COLOR_CODE}Using input file: {args.input}{RESET_COLOR_CODE}',
      file=sys.stdout, flush=True
    )

  # create an instance of the EvalStats class  
  eval_stats = EvalStats(
    data=data,
    num_workers=args.num_workers,
  )

  # compute the statistics based on the provided arguments
  if args.all:
    print(
      'Computing all statistics... ', 
      file=sys.stdout, flush=True, end='',
    )
    results = eval_stats.compute_all()
    
    # log the time taken to compute the statistics
    toc = now()
    print(
      f'{GREEN_COLOR_CODE}[DONE]{RESET_COLOR_CODE} took {toc - tic:.2f} seconds.',
      file=sys.stdout, flush=True
    )
  else:
    print(
      'Computing selected statistics...', 
      file=sys.stdout, flush=True, end='',
    )
    results = {}
    if args.mean:
      results['mean'] = eval_stats.mean()
    if args.std:
      results['std'] = eval_stats.std()
    if args.min:
      results['min'] = eval_stats.min()
    if args.max:
      results['max'] = eval_stats.max()
    if args.count:
      results['count'] = eval_stats.count()
    if args.sum:
      results['sum'] = eval_stats.sum()
    if args.variance:
      results['variance'] = eval_stats.variance()

    # log the time taken to compute the statistics
    toc = now()
    print(
      f'{GREEN_COLOR_CODE}[DONE]{RESET_COLOR_CODE} took {toc - tic:.2f} seconds.',
      file=sys.stdout, flush=True
    )

  # print the results
  if args.output:
    print(
      f'Saving results to {args.output}...', 
      file=sys.stdout, flush=True
    )
    # create the output file and write the results
    with open(args.output, 'w') as f:
      # loop through the results and write them to the file
      for key, value in results.items():
        f.write(f'{key}: {value}\n')
    # log the output file
    print(
      f'Results saved to {args.output}',
      file=sys.stdout, flush=True
    )
  # if no output file is provided, print the results to stdout
  else:
    print(f'{GREEN_COLOR_CODE}Computed Statistics{RESET_COLOR_CODE}', file=sys.stdout, flush=True)
    json.dump(
      results, 
      sys.stderr, 
      indent=2, 
      sort_keys=True,
    )
    print('', file=sys.stderr, flush=True)
    
if __name__ == '__main__':
  main()
