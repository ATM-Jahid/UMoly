#!/usr/bin/env xonsh

import argparse

parser = argparse.ArgumentParser(description='Move a group of files to a new directory!')
parser.add_argument('-i', '--input', default='niarg', metavar='', help='file identifier')
args = parser.parse_args()

mkdir -p @(args.input)
mv *.@(args.input)* @(args.input)/

# vim: ft=python
