#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from .__version__ import __version__

__author__ = ['Nico Curti']
__email__ = ['nico.curti2@unibo.it']

def parse_args():
  # global sofware information
  parser = argparse.ArgumentParser(
    prog='evalstats',
    argument_default=None,
    add_help=True,
    prefix_chars='-',
    allow_abbrev=True,
    exit_on_error=True,
    description='dummy project for the statistics evaluation',
  )

  parser.add_argument(
    '--version', '-v',
    dest='version',
    required=False,
    action='store_true',
    default=False,
    help='Get the current version installed',
  )

  args = parser.parse_args()
  return args

def main ():
  # extract the arguments of the cmd
  args = parse_args()
	
  if args.version:
  	print(__version__)

if __name__ == '__main__':
	main()
