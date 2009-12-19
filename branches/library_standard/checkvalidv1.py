# python -m doctest -v checkvalidv1.py

# Alex Leone (acleone ~AT~ gmail.com), 2009-12-06

"""Checks a generator to see if it is valid.

Definitions:
 "Board": a development board, eg. Arduino Diecimila.
 

"""

import re

def expand_range(s):
    r"""
    Expands a range in a string to a list of strings.  A range is defined as
    \d+:\d+, optionally surrounded by '{' and '}'.
    @param s string
    @return list[string]
    
    Examples:
    >>> expand_range("30:32")
    ['30', '31', '32']
    >>> expand_range("PB2:0")
    ['PB2', 'PB1', 'PB0']
    >>> expand_range("PB{0:3}999")
    ['PB0999', 'PB1999', 'PB2999', 'PB3999']
    >>> expand_range("PB4")
    ['PB4']
    """
    match = re.match(r'(.*?)(\d+):(\d+)(.*)', s)
    if not match:
        return [s]
    sbefore = match.group(1)
    safter = match.group(4)
    if sbefore.endswith('{') and safter.startswith('}'):
        sbefore = sbefore[:-1]
        safter = safter[1:]
    start = int(match.group(2))
    end = int(match.group(3))
    if start < end:
        nums = range(start, end + 1)
    else:
        nums = range(start, end - 1, -1)
    return [sbefore + str(i) + safter for i in nums]

def expand_all_ranges(strs):
    """
    Expands all range strings in a list of strings.
    @see expand_range(s)
    @param strs list[string] of ranges
    @return list[string] with ranges expanded
    
    Examples:
    >>> expand_all_ranges(["PB0:2", "PC4", "PD5:3"])
    ['PB0', 'PB1', 'PB2', 'PC4', 'PD5', 'PD4', 'PD3']
    """
    result = []
    for s in strs:
        result.extend(expand_range(s))
    return result

def expand_all_ranges_dict(d):
    """
    Expands all the range strings in a dictionary of {string:string}.
    @see expand_range(s)
    @param d dict[string:string] of ranges
    @return dict[string:string] with ranges expanded
    @throws IndexError if a key's range doesn't match a value's range
    
    Examples:
    >>> expand_all_ranges_dict({"1:3": "PB0:2", "4": "PC0"})
    {'1': 'PB0', '3': 'PB2', '2': 'PB1', '4': 'PC0'}
    """
    newks = []
    newvs = []
    for k, v in d.iteritems():
        krange = expand_range(k)
        vrange = expand_range(v)
        if len(krange) != len(vrange):
            raise IndexError(
                "len(expand_range({0})) ({1}) != len(expand_range({2})) ({3})"
                .format(repr(k), len(krange), repr(v), len(vrange)) )
        newks.extend(krange)
        newvs.extend(vrange)
    return dict(zip(newks, newvs))
    
def make_pin_map(d):
    """
    Makes a dict of pin_name : list[pin_num].
    @param d dict[string:string] pin_num : pin_name
    @return dict[string:list[string]] pin_name : list[pin_num]
    
    Examples:
    >>> make_pin_map({"1:3": "PB0:2", "4": "PC0"})
    {'PC0': ['4'], 'PB1': ['2'], 'PB0': ['1'], 'PB2': ['3']}
    """
    expanded = expand_all_ranges_dict(d)
    pin_map = {}
    for pin_num, pin_name in expanded.iteritems():
        if pin_name in pin_map:
            pin_map[pin_name].append(pin_num)
        else:
            pin_map[pin_name] = [pin_num]
    return pin_map
    
    
def is_valid_pin_map(pin_map, pin_names):
    """
    Checks too see if all pin names appear at least once, there's no repeated
    pin numbers in the pin map, and no keys in pin_map that aren't in pin_names.
    @param pin_map dict[string:list[string]] pin_name : list[pin_num]
    @param pin_names list[string] pin names
    @return list[string] of errors
    
    Examples:
    >>> is_valid_pin_map({"PB2": ["4"], "VCC": ["2"]}, ["PB2", "VCC"])
    []
    >>> is_valid_pin_map({"PB2": ["4"]}, ["PB2", "VCC"])
    ["'VCC' is not listed in the pin_map!"]
    >>> is_valid_pin_map({"PB2": ["4"], "VCC": ["4"]}, ["PB2", "VCC"])
    ["'4' is mapped twice - second time is 'PB2':'4'!"]
    >>> is_valid_pin_map({"GND": ["5"], "PB2": ["4"]}, ["PB2"])
    ["'GND' does not appear in pin_names!"]
    """
    not_seen_names = dict(zip(pin_names, [None] * len(pin_names)))
    seen_pin_nums = {}
    errors = []
    for pin_name, pin_nums in pin_map.iteritems():
        if pin_name not in pin_names:
            errors.append(repr(pin_name) + " does not appear in pin_names!")
        if pin_name in not_seen_names:
            del not_seen_names[pin_name]
        for pin_num in pin_nums:
            if pin_num in seen_pin_nums:
                errors.append("{0} is mapped twice - second time is {1}:{0}!"
                              .format(repr(pin_num), repr(pin_name)))
            seen_pin_nums[pin_num] = None
    errors.extend([repr(pin_name) + " is not listed in the pin_map!"
                   for pin_name in not_seen_names])
    return errors
        

common_pin_names = [
    "VCC",
    "GND",
    "PB7:0",
    "PC6:0",
    "PD7:0",
    "AVCC",
    "AREF",
]

pin_names_28 = expand_all_ranges(common_pin_names)
pin_names_32 = expand_all_ranges(common_pin_names + ["ADC7:6"])

chip_ATmega48_88_168_328 = {
    "packages": {
        "TQFP": {
            "pin_names": pin_names_32,
            "pin_map": make_pin_map({
                "1:2"  : "PD3:4",
                "3"    : "GND",
                "4"    : "VCC",
                "5"    : "GND",
                "6"    : "VCC",
                "7:8"  : "PB6:7",
                "9:11" : "PD5:7",
                "12:17": "PB0:5",
                "18"   : "AVCC",
                "19"   : "ADC6",
                "20"   : "AREF",
                "21"   : "GND",
                "22"   : "ADC7",
                "23:29": "PC0:6",
                "30:32": "PD0:2",
            }),
        },
        "PDIP": {
            "pin_names": pin_names_28,
            "pin_map": make_pin_map({
                "1"    : "PC6",
                "2:6"  : "PD0:4",
                "7"    : "VCC",
                "8"    : "GND",
                "9:10" : "PB6:7",
                "11:13": "PD5:7",
                "14:19": "PB0:5",
                "20"   : "AVCC",
                "21"   : "AREF",
                "22"   : "GND",
                "23:28": "PC0:5",
            }),
        },
        "28 MLF": {
            "pin_names": pin_names_28,
            "pin_map": make_pin_map({
                "1:2"  : "PD3:4",
                "3"    : "VCC",
                "4"    : "GND",
                "5:6"  : "PB6:7",
                "7:9"  : "PD5:7",
                "10:15": "PB0:5",
                "16"   : "AVCC",
                "17"   : "AREF",
                "18"   : "GND",
                "19:25": "PC0:6",
                "26:28": "PD0:2",
            }),
        },
        "32 MLF": {
            "pin_names": pin_names_32,
            "pin_map": make_pin_map({
                "1:2"  : "PD3:4",
                "3"    : "GND",
                "4"    : "VCC",
                "5"    : "GND",
                "6"    : "VCC",
                "7:8"  : "PB6:7",
                "9:11" : "PD5:7",
                "12:17": "PB0:5",
                "18"   : "AVCC",
                "19"   : "ADC6",
                "20"   : "AREF",
                "21"   : "GND",
                "22"   : "ADC7",
                "23:29": "PC0:6",
                "30:32": "PD0:2",
            }),
        },
    },
    
    "alt_pin_function_names": {
        "PB7": ["XTAL2", "TOSC2", "PCINT7"],
        "PB6": ["XTAL1", "TOSC1", "PCINT6"],
        "PB5": ["SCK", "PCINT5"],
        "PB4": ["MISO", "PCINT4"],
        "PB3": ["MOSI", "OC2A", "PCINT3"],
        "PB2": ["SS", "OC1B", "PCINT2"],
        "PB1": ["OC1A", "PCINT1"],
        "PB0": ["ICP1", "CLKO", "PCINT0"],
        
        "PC6": ["RESET", "PCINT14"],
        "PC5": ["ADC5", "SCL", "PCINT13"],
        "PC4": ["ADC4", "SDA", "PCINT12"],
        "PC3": ["ADC3", "PCINT11"],
        "PC2": ["ADC2", "PCINT10"],
        "PC1": ["ADC1", "PCINT9"],
        "PC0": ["ADC0", "PCINT8"],
        
        "PD7": ["AIN1", "PCINT23"],
        "PD6": ["AIN0", "OC0A", "PCINT22"],
        "PD5": ["T1", "OC0B", "PCINT21"],
        "PD4": ["XCK", "T0", "PCINT20"],
        "PD3": ["INT1", "OC2B", "PCINT19"],
        "PD2": ["INT0", "PCINT18"],
        "PD1": ["TXD", "PCINT17"],
        "PD0": ["RXD", "PCINT16"],
    },

    "versions": {
        "ATmega48": {
            "flash": 4000,
            "eeprom": 256,
            "ram": 512,
        },
        "ATmega88": {
            "flash": 8000,
            "eeprom": 512,
            "ram": 1024,
        },
        "ATmega168": {
            "flash": 16000,
            "eeprom": 512,
            "ram": 1024,
        },
        "ATmega328": {
            "flash": 32000,
            "eeprom": 1024,
            "ram": 2048,
        },
    },
}

devboard_Arduino = {
    "chip": chip_ATmega48_88_168_328,
    "pin_names": expand_all_ranges_dict({
        "PD0:7": "digital0:7",
        "PB0:5": "digital8:13",
        "PC0:5": "analog0:5",
        "VCC"  : "+5V",
        "GND"  : "GND",
        "AREF" : "AREF",
        "PC6"  : "RESET",
    }),
}

example = {
    # when to use this code
    "board_defines": ["__ARDUINO__"],
    "mcu_defines": ["__AVR_ATmega48__"],
    
    #
}


def test(generator):
    assert 'board_defines' in generator
    assert 'mcu_defines' in generator
    

