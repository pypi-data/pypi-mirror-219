#! /usr/bin/env python3

import klassez as pkg
from klassez import *
from inspect import isfunction


modules = 'misc', 'processing', 'figures', 'sim', 'fit', 'Spectra'

sys.stdout = open('fcn_list.txt', 'w')
for module in modules:
    print(f'{module.upper()}')
    M_dict = pkg.__dict__[module].__dict__
    M_func = sorted([func_name for func_name in M_dict.keys() if isfunction(M_dict[func_name])])
    print(*[f' {func}\n' for func in M_func])
    print('\n')
