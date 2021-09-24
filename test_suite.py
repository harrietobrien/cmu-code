#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 22:50:49 2019

@author: harrietobrien
"""

import sys
sys.path.append('Genarris_Development/src/generation/')
sys.path.append('Genarris_Development/src/utilities/')
sys.path.append('Genarris_Development/src/core/')
sys.path.append('Genarris_Development/src/core/')
sys.path.append('.')
from Genarris_Development.src.generation import sgroup, generation_util
from Genarris_Development.src.core import structure_handling 
from sgroup import Sgroup
from generation_util import place_molecule_space_group, StructureGenerator
from Genarris_Development.src.core import structure 
from structure import Structure
import test_suite_settings
import inspect

class TestGenarris(object):
    
    def __init__(self):
        for attribute in vars(test_suite_settings).keys():
            if not attribute:
                pass
            setattr(self, attribute, vars(test_suite_settings)[attribute])
        if not self.options:
            print('No function(s) selected.')
        self.functions = {}
        for function in self.options:
            try:
                self.functions[function] = eval('self.' + function)
            except:
                print(('The function %s does not exist') % function)
        self.args_dict = {'generate_structure' : StructureGenerator} 
        self.output_filter()

    def output_space_groups(self):
        if not self.include_space_groups:
            space_groups = list(range(1,143))
            for i in self.exclude_space_groups:
                space_groups.remove(i)
        else:
            space_groups= list()
            for i in self.include_space_groups:
                if i in list(range(1,143)):
                    space_groups.append(i)
            for j in self.exclude_space_groups:
                if j in list(range(1,143)) and j in space_groups:
                    space_groups.remove(j)
        setattr(self, 'space_groups', space_groups)

    # runs whatever functions specified in settings
    def test_genarris(self):
        for selection in self.options:
            if selection in self.functions.keys():
                self.functions[selection](self.settings[selection])
    
    def get_args(self):
        write_dict = dict()
        for i in self.args_dict:
            spec = self.get_attributes(self.args_dict[i])
            op_args = spec.args
            op_args.remove('self')
            write_dict[i] = op_args
        f = open('args.txt', 'w+')
        for j in write_dict:
            f.write(j + 2*'\n')
            for k in write_dict[j]:
                f.write(k + '\n')
    
    def output_filter(self):
        if hasattr(self, 'output_structures'):
            if self.output_structures:
                # self.output = 
                pass
            else:
                pass
                # self.output = 
        if hasattr(self, 'include_space_groups') and \
           hasattr(self, 'exclude_space_groups'):
            self.output_space_groups()
        if hasattr(self, 'output_point_groups'):
            pass
        if hasattr(self, 'output_struct_by'):
            pass
    
    def get_attributes(self, cls):
        return inspect.getfullargspec(cls.__init__)

    def generate_structure(self):
        # inspect
        spec = self.get_attributes(StructureGenerator)
        # create ordered dict
        dflt_order = dict()
        for i in range(len(spec.defaults)):
            dflt_order[i+1] = spec.defaults[i]
        # dict for changing kw defaults
        dflt_dict = dict(zip(spec.args[::-1],(spec.defaults or ())[::-1]))
        # create arg dict with spec
        args = dict()
        for arg in spec.args:
            if arg not in dflt_dict and arg != "self":
                args[arg] = None
        # fill arg dict with values from settings 
        # change any kw default values needed
        for arg in self.settingsdb["generate_structure"]:
            if arg in args.keys():
                args[arg] = self.settingsdb['generate_structure'][arg]
            elif arg in dflt_dict and arg not 4n args:
                dflt_dict[arg] = self.settingsdb['generate_structure'][arg]
        if dflt_dict['molecule'] == None:
            molecule_path = 'GIYHUR_molecule.in'
            molecule_obj = Structure()
            molecule_obj.build_geo_from_atom_file(molecule_path)
            dflt_dict["molecule"] = molecule_obj
        space_groups = list(range(143))
        space_groups.remove(0)
        space_groups.remove(1)
        for sgn in space_groups:
            struct = Structure()
            tmp = Sgroup(sgn)
            dflt_dict["space_groups_allowed"] = [sgn]
            dflt_dict["output_dir"] = './test_structures'
            args["nmpc"] = tmp.wmult[0]    
            # make a list of arg vals
            arg_vals = list()
            for arg in args.values():
                arg_vals.append(arg)
            generator = StructureGenerator(*arg_vals, **dflt_dict)
            struct = generator.generate_structure()
            #struct.get_space_group_number()
            print(struct)
            
if __name__ == '__main__':
    test = TestGenarris()
    #print(test.output_point_groups)
    test.generate_structure()