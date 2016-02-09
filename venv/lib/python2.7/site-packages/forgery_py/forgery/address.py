# -*- coding: utf-8 -*-
# Copyright (C) 2012 by Tomasz Wójcik <labs@tomekwojcik.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Generate forged addres-related data."""

import random
import string

from ..dictionaries_loader import get_dictionary

__all__ = [
    'street_name', 'street_number', 'street_suffix', 'street_address',
    'city', 'state', 'state_abbrev', 'zip_code', 'phone', 'country',
    'continent'
]


def street_name():
    """Random street name."""
    return random.choice(get_dictionary('street_names')).strip()


def street_number():
    """Random street number."""
    length = int(random.choice(string.digits[1:6]))
    return ''.join(random.sample(string.digits, length))


def street_suffix():
    """Random street suffix."""
    return random.choice(get_dictionary('street_suffixes')).strip()


def street_address():
    """
    Random street address. Equivalent of ``street_number() + ' ' + 
    street_name() + ' ' + street_suffix()``.
    """
    return '%s %s %s' % (street_number(), street_name(), street_suffix())


def city():
    """Random city name."""
    return random.choice(get_dictionary('cities')).strip()


def state():
    """Random US state name."""
    return random.choice(get_dictionary('states')).strip()


def state_abbrev():
    """Random US abbreviated state name."""
    return random.choice(get_dictionary('state_abbrevs')).strip()


def zip_code():
    """Random ZIP code, either in `#####` or `#####-####` format."""
    format = '#####'
    if random.random() >= 0.5:
        format = '#####-####'

    result = ''
    for item in format:
        if item == '#':
            result += str(random.randint(0, 9))
        else:
            result += item

    return result


def phone():
    """Random phone number in `#-(###)###-####` format."""
    format = '#-(###)###-####'

    result = ''
    for item in format:
        if item == '#':
            result += str(random.randint(0, 9))
        else:
            result += item

    return result


def country():
    """Random country name."""
    return random.choice(get_dictionary('countries')).strip()


def continent():
    """Random continent name."""
    return random.choice(get_dictionary('continents')).strip()
