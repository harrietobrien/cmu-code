#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 20:13:31 2018

@author: harrietobrien
"""

import json

def sort_by_hall(filename):
    with open(filename,'r') as csvfile:
        csvf_by_lines = [line for line in csvfile]
        sort_by_hall_number = []
        current_hall_number = []
        for line in csvf_by_lines:
            if line[0].isdigit() and line!=csvf_by_lines[0]:
                sort_by_hall_number.append(current_hall_number)
                current_hall_number = []
                current_hall_number.append(line)
            elif line.startswith('end'):
                sort_by_hall_number.append(current_hall_number)
                break
            else:
                current_hall_number.append(line)
        return sort_by_hall_number

def parse_hall_list(hall_list):
    hall_number_dict = dict()
    for hall_string_list in hall_list:
        multiplicity_list = []
        wyckoff_letter_list = []
        site_symmetry_list = []
        coordinate_list = []
        tmp_coordinate_list_1 = []
        tmp_coordinate_list_2 = []
        for hall_string in hall_string_list:
            if hall_string[0].isdigit():
                tmp_coordinate_list_1 = []
                hall_number = hall_string.split(':')[0]
                hall_number_dict[hall_number] = {}
                space_group = hall_string.split(':')[1]
                hall_number_dict[hall_number]['Space Group'] = space_group
            else:
                line_continued = False
                if hall_string.startswith('::::'):
                    line_continued = True
                    for element in hall_string.split(':')[5:]:
                        if element.startswith('('):
                            element = element.replace('\n','')
                            tmp_coordinate_list_2.extend([element])
                elif hall_string.startswith('::'):
                    if tmp_coordinate_list_2 != []:
                        tmp_coordinate_list_1.append(tmp_coordinate_list_2)
                        tmp_coordinate_list_2 = []
                    multiplicity_list.append(hall_string.split(':')[2])
                    wyckoff_letter_list.append(hall_string.split(':')[3])
                    site_symmetry_list.append(hall_string.split(':')[4])
                    for element in hall_string.split(':')[5:]:
                        if element.startswith('('):
                            element = element.replace('\n','')
                            tmp_coordinate_list_2.append(element)
                if not line_continued:
                    coordinate_list.append(tmp_coordinate_list_2)
        hall_number_dict[hall_number]['Multiplicity'] = multiplicity_list
        hall_number_dict[hall_number]['Wyckoff Letter'] = wyckoff_letter_list
        hall_number_dict[hall_number]['Site Symmetry'] = site_symmetry_list
        hall_number_dict[hall_number]['Coordinates'] = coordinate_list
    return hall_number_dict

def dict_to_json(spglib_database):
    with open('spglib_database.json','w') as jsonfile:
        json.dump(spglib_database, jsonfile, sort_keys=True, indent=4, separators=(',', ': '))
    
if __name__ == "__main__":
    csv_file = '/Users/harrietobrien/Desktop/spglib_test/database/database/Wyckoff.csv'
    hall_list = sort_by_hall(csv_file)
    spglib_database = parse_hall_list(hall_list)
    dict_to_json(spglib_database)
    
    
    




