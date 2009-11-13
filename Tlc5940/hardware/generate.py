#!/usr/bin/env python

# Copyright (c) 2009 by Alex Leone <acleone ~AT~ gmail.com>
#
# This file is part of the Arduino TLC5940 Library.
#
# The Arduino TLC5940 Library is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# The Arduino TLC5940 Library is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with The Arduino TLC5940 Library.  If not, see
# <http://www.gnu.org/licenses/>.

"""
See example.py for how to add boards to the library.

This file finds *.py files in this directory, looks for a dict named
'generator' which has all the information to generate tlc_{filename}.h,
and finally generates "tlc_board_select.h" which will conditionally include
the right header file for each chip.
"""

import os
import sys
import re

import mcu_order

FILE_EXT = '.py'
SKIP = ('generate.py', 'example.py', 'mcu_order.py', 'default.py')

class ErrorPrinter:
    """Prints 'In {filename}:' before the first error message."""
    def __init__(self, filename):
        self.filename = filename
        self.is_filename_printed = False
        
    def show(self, msg):
        if not self.is_filename_printed:
            self.is_filename_printed = True
            print "In '{0}':".format(self.filename)
        print msg

def module_to_h_name(modulename):
    return "tlc_" + modulename + ".h"

def write_mcu_order(macro, modulename):
    """
    Adds items to the mcu_order dictionary in mcu_order.py by editing the file.
    """
    re_str = r"(\s*)mcu_order\s*=\s*{"
    p = re.compile(re_str)
    mcu_order_file = open('mcu_order.py', 'r')
    lines = mcu_order_file.readlines()
    insert_line = -1
    for i, line in enumerate(lines):
        m = p.match(line)
        if m != None:
            insert_line = i
            break
    if insert_line == -1:
        print "Error: '{0}' not found in mcu_order.py!".format(re_str)
        mcu_order_file.close()
        return
    mcu_order_file.close()
    lines.insert(insert_line + 1, "{0}    '{1}': '{2}',\n".format(
        m.group(1), macro, modulename,
    ))
    mcu_order_file = open('mcu_order.py', 'w')
    mcu_order_file.writelines(lines)
    mcu_order_file.close()

class BoardSelectGenerator:
    """
    Generates tlc_board_select.h which will include the right board.
    To generate the .h file, it uses generator['board_macros' & 'mcu_macros']
    and mcu_macros.py for additional default ordering.
    """
    def __init__(self):
        self.defined_macros = {}
        
    def add_board(self, generator, modulename, error):
        for macro in generator['board_macros']:
            if macro in self.defined_macros:
                error.show(
                    "Error: board_macro '{0}' defined in both '{1}' " \
                    "and '{2}'!".format(
                        macro,
                        self.defined_macros[macro] + FILE_EXT,
                        modulename + FILE_EXT,
                    )
                )
            else:
                self.defined_macros[macro] = modulename
        for macro in generator['mcu_macros']:
            if macro in self.defined_macros:
                # this mcu macro, eg '__AVR_ATmega168__' is already used by a
                # board, so we need to specify which board gets the include by
                # default. So if the 'board_macro', eg '__MY_SPIFFY_DEV_BOARD__'
                # is not defined, the board in mcu_order.py gets the include.
                if macro not in mcu_order.mcu_order:
                    prev_define_modulename = self.defined_macros[macro]
                    s = "Warning: mcu_macro '{0}' defined in both '{1}'" \
                        " and '{2}', but not defined in mcu_order.py! " \
                        "Giving priority to '{1}' and overwriting " \
                        "mcu_order.py." 
                    print s.format(
                        macro,
                        prev_define_modulename + FILE_EXT,
                        modulename + FILE_EXT,
                    )
                    write_mcu_order(macro, prev_define_modulename)
                    mcu_order.mcu_order[macro] = self.defined_macros[macro]
                if mcu_order.mcu_order[macro] == modulename:
                    self.defined_macros[macro] = modulename
            else:
                self.defined_macros[macro] = modulename

def check_spi_mode_ordering(spi_modes, spi_modes_order, error):
    """
    Check that all the keys in 'spi_modes' are in 'spi_modes_order'
    and vice-versa.
    Returns: True if valid, False otherwise.
       
    >>> error = ErrorPrinter('<doctest string>')
    >>> modes = {'spi': None, 'usart': None, 'bitbang': None}
    >>> modes_order = ['usart', 'spi', 'bitbang']
    >>> check_spi_mode_ordering(modes, modes_order, error)
    True
    >>> modes_order[0] = 'usarT'
    >>> check_spi_mode_ordering(modes, modes_order, error)
    In '<doctest string>':
    Error: 'usarT' is in 'spi_modes_order' but doesn't exist in 'spi_modes'!
    Error: 'usart' is in 'spi_modes' but doesn't exist in 'spi_modes_order'!
    False
    """
    error_str = "Error: '{0}' is in '{1}' but doesn't exist in '{2}'!"
    valid = True
    in_order = {}
    for mode in spi_modes_order:
        if mode not in spi_modes:
            error.show(error_str.format(
                mode, 'spi_modes_order', 'spi_modes',
            ))
            valid = False
        else:
            in_order[mode] = None
    for mode in spi_modes:
        if mode not in in_order:
            error.show(error_str.format(
                mode, 'spi_modes', 'spi_modes_order',
            ))
            valid = False
    return valid
                
    
def spi_generator(generator, error):
    """
    Returns a list of strings that should be written to the board.h file,
            or False if there was an error in the spi_modes.
    """
    spi_modes = generator['spi_modes']
    spi_modes_order = generator['spi_modes_order']
    if not check_spi_mode_ordering(spi_modes, spi_modes_order, error):
        return False
    mode_defines = []
    all_mode_defines = []
    modes_code = []
    for mode in spi_modes_order:
        mode_define = "TLC_SPI_MODE_" + mode.upper()
        mode_defines.append(mode_define)
        defined_check = "defined(" + mode_define + ")"
        all_mode_defines.append(defined_check)
        modes_code.extend((
            "#if ", defined_check, "\n",
            spi_modes[mode]['code'], "\n",
            "#endif /* ", defined_check, " */\n\n\n",
        ))
                           
    all_mode_defines = " + ".join(all_mode_defines)
    result = [
        "#if ", all_mode_defines, " > 1\n",
        "#  error at most 1 spi mode can be defined: ", str(mode_defines), "\n",
        "#elif ", all_mode_defines, " == 0\n",
        "#  define ", mode_defines[0], "\n",
        "#endif\n\n",
    ]
    result.extend(modes_code)
    return result


def generate():
    generators = {}
    board_select_gen = BoardSelectGenerator()
    for f in sorted(os.listdir(sys.path[0])):
        if f.endswith(FILE_EXT) and f not in SKIP:
            error = ErrorPrinter(f)
            modulename = f[:-len(FILE_EXT)]
            module = __import__(modulename)
            if 'generator' not in dir(module):
                error.show("No 'generator' variable defined!")
                continue
            generator = module.generator
            generators[modulename] = generator
            board_select_gen.add_board(generator, modulename, error)
            spi_code_list = spi_generator(generator, error)
            if not spi_code_list:
                continue
            board_h_name = module_to_h_name(modulename)
            board_h_define = board_h_name.upper().replace(".", "_")
            board_h_file = open(board_h_name, "w")
            board_h_file.write(
                "#if !defined(" + board_h_define + ")\n" \
                "#    define  " + board_h_define + "\n\n"
            )
            for s in spi_code_list:
                board_h_file.write(s)
            board_h_file.write(
                "#endif /* !defined(" + board_h_define + ") */\n\n"
            )
            board_h_file.close()
                    

if __name__ == '__main__':
    generate()  
    
