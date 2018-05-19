#!/usr/bin/env python3

import csv
import sys
import re
from shutil import copyfile

input_file = sys.argv[1]
output_file = '/tmp/2_realty.csv'
column_index = 1

lstrip_chars = ' \t,-.'
rstrip_chars = ' \t,-'

repeating_pattern = r'(\s?)([\s.,])\2+'
repeating_replacement = r'\2'
repeating_re = re.compile(repeating_pattern)

dot_pattern = r'(\s?)([,.])([Є-ЯҐа-їґ0-9])'
dot_re = re.compile(dot_pattern)
dot_replacement = r'\2 \3'

index_pattern = r'^([0-9]{1,})'
index_re = re.compile(index_pattern)

with open(input_file) as csvfileforread, open(output_file, 'w') as csvfileforwrite:
    input_file_object = csv.reader(csvfileforread, delimiter=',', quotechar='"')
    output_file_object = csv.writer(csvfileforwrite, delimiter=',', quotechar='"')
    for row in input_file_object:
        row[column_index] = index_re.sub('', row[column_index]).lstrip(lstrip_chars).rstrip(rstrip_chars)
        if row[column_index].startswith('Україна'):
            row[column_index] = row[column_index].replace('Україна,', '', 1).lstrip(lstrip_chars).rstrip(rstrip_chars)
            row[column_index] = index_re.sub('', row[column_index]).lstrip(lstrip_chars).rstrip(rstrip_chars)
        row[column_index] = repeating_re.sub(repeating_replacement, row[column_index]).lstrip(lstrip_chars).rstrip(rstrip_chars)
        row[column_index] = dot_re.sub(dot_replacement, row[column_index])
        output_file_object.writerow(row)
copyfile(output_file, input_file)
