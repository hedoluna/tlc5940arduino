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

def module_to_h_filename(modulename):
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

class HfileGenerator:
    """
    Generates .h files with #if defined({filename}_H) guards to prevent multiple
    inclusion.
    """
    def __init__(self, filename):
        """Creates a new file and adds the include guard."""
        h_define = filename.upper().replace(".", "_")
        h_file = open(filename, "w")
        h_file.write(
            "#if !defined(" + h_define + ")\n" \
            "#    define  " + h_define + "\n\n"
        )
        self.h_define = h_define
        self.h_file = h_file
    
    def write(self, s):
        """Writes a string to the file."""
        self.h_file.write(s)
    
    def close(self):
        """Adds the end of the include guard and closes the file."""
        self.h_file.write(
            "#endif /* !defined(" + self.h_define + ") */\n\n"
        )
        self.h_file.close()
        

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

    def generate_selector_h(self, h_filename):
        boards = {}
        for macro in self.defined_macros:
            include_filename = module_to_h_filename(self.defined_macros[macro])
            if include_filename not in boards:
                boards[include_filename] = [macro]
            else:
                boards[include_filename].append(macro)
        select_h = HfileGenerator(h_filename)
        board_ifs = []
        for filename in boards:
            define_checks = ["defined({0})".format(s) for s in boards[filename]]
            board_ifs.append(
                '  \\\n || '.join(define_checks) + \
                '\n#  include "{0}"\n'.format(filename)
            )
        select_h.write("#if ")
        select_h.write("#elif ".join(board_ifs))
        select_h.write(
            "#else\n" \
            "#  error Board not recognized! Please send an email " \
            "to acleone ~AT~ gmail.com to add support for your board.\n" \
            "#endif\n\n"
        )
        select_h.close()
        
                  
    
def mode_generator(generator, modes_str, order_str, define_prefix, error):
    """
    Returns a list of strings that should be written to the board.h file.
    
    >>> error = ErrorPrinter('<string>')
    >>> g = {
    ...     'mode_order': ('a', 'b'),
    ...     'modes': {
    ...         'a': {'pins': (), 'code': "mode a"},
    ...         'b': {'pins': (), 'code': "mode b"},
    ...     },
    ... }
    >>> slist = mode_generator(g, 'modes', 'mode_order', 'TLC_', error)
    >>> print "".join(slist)
    #if defined(TLC_A) \\
          + defined(TLC_B) > 1
    #  error at most 1 mode can be defined of: ['TLC_A', 'TLC_B']
    #elif defined(TLC_A) \\
          + defined(TLC_B) == 0
    #  define TLC_A
    #endif
    <BLANKLINE>
    #if defined(TLC_A)
    mode a
    #endif /* defined(TLC_A) */
    <BLANKLINE>
    <BLANKLINE>
    #if defined(TLC_B)
    mode b
    #endif /* defined(TLC_B) */
    <BLANKLINE>
    <BLANKLINE>
    <BLANKLINE>
    >>> del g['modes']['a']
    >>> del g['modes']['b']
    >>> slist = mode_generator(g, 'modes', 'mode_order', 'TLC_', error)
    In '<string>':
    Warning: 'a' is in 'mode_order' but not in 'modes'!
    Warning: 'b' is in 'mode_order' but not in 'modes'!
    Error: No valid modes in 'modes'!
    >>> slist == []
    True
    """
    modes = generator[modes_str]
    modes_order = generator[order_str]
    mode_defines = []
    all_mode_defines = []
    modes_code = []
    for mode in modes_order:
        if mode not in modes:
            error.show(
                "Warning: '{0}' is in '{1}' but not in '{2}'!".format(
                    mode, order_str, modes_str,
                )
            )
            continue                       
        mode_define = define_prefix + mode.upper()
        mode_defines.append(mode_define)
        defined_check = "defined(" + mode_define + ")"
        all_mode_defines.append(defined_check)
        modes_code.extend((
            "#if ", defined_check, "\n",
            modes[mode]['code'], "\n",
            "#endif /* ", defined_check, " */\n\n\n",
        ))
    if len(mode_defines) == 0:
        error.show("Error: No valid modes in '{0}'!".format(modes_str))
        return []
    all_mode_defines = " \\\n      + ".join(all_mode_defines)
    result = [
        "#if ", all_mode_defines, " > 1\n",
        "#  error at most 1 mode can be defined of: ", str(mode_defines), "\n",
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
            spi_code_list = mode_generator(
                generator,
                'spi_modes', 'spi_modes_order', 'TLC_SPI_MODE_',
                error,
            )
            timer_code_list = mode_generator(
                generator,
                'timer_modes', 'timer_modes_order', 'TLC_TIMER_MODE_',
                error,
            )
            board_h_name = module_to_h_filename(modulename)
            board_h = HfileGenerator(board_h_name)
            for s in spi_code_list:
                board_h.write(s)
            for s in timer_code_list:
                board_h.write(s)
            board_h.close()
    board_select_gen.generate_selector_h('tlc_board_select.h')
                    

if __name__ == '__main__':
    generate()  
    
