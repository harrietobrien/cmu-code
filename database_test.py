#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 17:27:38 2018

@author: harrietobrien
"""

from spglib_database import spglib_database
from parse_wyckoff_csv import sort_by_hall

def csv_lines(filename):
    with open(filename,'r') as csvfile:
        csv_lines = [line for line in csvfile]
    return csv_lines

def verify_hall_numbers():
    expected_hall_numbers = set(range(531))
    expected_hall_numbers.discard(0)
    hall_numbers = set()
    for hall_number in spglib_database:
        hall_numbers.add(eval(hall_number))
    print(' '.join(["Database contains hall numbers 1-530 and these keys only",
          "..."]), end="")
    assert(hall_numbers == expected_hall_numbers)
    assert(len(hall_numbers) == 530)
    print("Passed.")

def verify_space_groups():
    hall_number_csv_lines = []
    for line in csv_lines:
        if line[0].isdigit():
            hall_number_csv_lines.append(line)
    assert(len(hall_number_csv_lines) == 530)
    int_hall_numbers = []
    for hall_number in spglib_database:
        int_hall_numbers.append(int(hall_number))
    sorted_int_hall_numbers = sorted(int_hall_numbers)
    verify_space_groups.sorted_string_hall_numbers = []
    for hall_number in sorted_int_hall_numbers:
        verify_space_groups.sorted_string_hall_numbers.append(str(hall_number))
    assert(len(verify_space_groups.sorted_string_hall_numbers) == 530)
    built_comparison_lines = []
    for hall_number in verify_space_groups.sorted_string_hall_numbers:
        create_line = '%s:%s:::::::\n'%(hall_number,spglib_database
                                      [hall_number]['Space Group'])
        built_comparison_lines.append(create_line)
    assert(len(built_comparison_lines) == 530)
    print(' '.join(["All hall numbers correspond to their respective space",
                    "groups ..."]), end="")
    assert(hall_number_csv_lines == built_comparison_lines)
    print("Passed.")

def verify_mult_letter_site():
    sort_by_hall_number = sort_by_hall(csv_file)
    partitioned_double_colon_lines = []
    for hall_number in sort_by_hall_number:
        tmp_double_colon_lines = []
        for line in hall_number:
            if not line.startswith('::::') and line.startswith('::'):
                tmp_double_colon_lines.append(line.partition('(')[0])
        partitioned_double_colon_lines.append(tmp_double_colon_lines)
    built_comparison_lines = []
    for hall_number in verify_space_groups.sorted_string_hall_numbers:
        tmp_comparison_lines = []
        for mult in range(len(spglib_database[hall_number]['Multiplicity'])):
            create_line = '::%s:%s:%s:'%(
                        spglib_database[hall_number]['Multiplicity'][mult],
                        spglib_database[hall_number]['Wyckoff Letter'][mult],
                        spglib_database[hall_number]['Site Symmetry'][mult])
            tmp_comparison_lines.append(create_line)
        built_comparison_lines.append(tmp_comparison_lines)
    print(' '.join(["Database includes correct multiplicities, Wyckoff letters,"
             " and site symmetries for each hall number ..."]), end="")
    assert(partitioned_double_colon_lines == built_comparison_lines)
    print("Passed.")
    print(' '.join(["(i.e. Partitioned csv lines (isolating multiplicities,",
          "Wyckoff letters, and site symmetries) and lines constructed",
          "from database information for comparison are identical)"]))

def get_sorted_string_hall_numbers():
    return verify_space_groups.sorted_string_hall_numbers

if __name__ == '__main__':
    csv_file = '/Users/harrietobrien/Desktop/spglib_test/database/database/Wyckoff.csv'
    csv_lines = csv_lines(csv_file)
    verify_hall_numbers()
    verify_space_groups()
    verify_mult_letter_site()
