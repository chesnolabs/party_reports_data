#!/usr/bin/env python3

import tablib, sys
from pib_regexp import *

NAME_COL = 3
CORRECT = [line.rstrip(",\n") for line in open('correct.csv', 'r').readlines()]
SUBSTITUTIONS = tablib.Dataset().load(open('substitute.csv').read())


def open_file(file):
    imported_file = tablib.Dataset().load(open(file).read())
    return imported_file


def substitution(imported_file):
    for row in imported_file:
        if row[8] == 'фізична особа':
            name = clean_field(row[NAME_COL])
            name = match_name_parts(name)['given_name']
            if name not in CORRECT:
                name = name.title()
            if name not in CORRECT:
                print(name)
    return imported_file

def write_file(tmp, substituted_file):
    with open(tmp, 'w') as f:
        f.write(substituted_file.export('csv'))

imported_file = open_file('2017/ОБ/5_donations.csv')
#imported_file = open_file(sys.argv[1])
substituted_file = substitution(imported_file)
write_file('2017/ОБ/5_tmp.csv', substituted_file)
#write_file(sys.argv[2], substituted_file)
