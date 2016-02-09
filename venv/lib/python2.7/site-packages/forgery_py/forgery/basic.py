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

"""Generate misc random data."""

import random
import string

HEX_DIGITS = string.hexdigits[:-6].upper()

__all__ = ['hex_color', 'hex_color_short', 'text']


def hex_color():
    """Random HEX color."""
    return ''.join(random.sample(HEX_DIGITS, 6))


def hex_color_short():
    """Random short (e.g. `FFF` color)."""
    return ''.join(random.sample(HEX_DIGITS, 3))


def text(length=None, at_least=10, at_most=15, lowercase=True,
         uppercase=True, digits=True, spaces=True, punctuation=False):
    """
    Random text.

    If `length` is present the text will be exactly this chars long. Else the
    text will be something between `at_least` and `at_most` chars long.
    """
    base_string = ''
    if lowercase:
        base_string += string.ascii_lowercase

    if uppercase:
        base_string += string.ascii_uppercase

    if digits:
        base_string += string.digits

    if spaces:
        base_string += ' '

    if punctuation:
        base_string += string.punctuation

    if len(base_string) == 0:
        return ''

    if not length:
        length = random.randint(at_least, at_most)

    result = ''
    for i in xrange(0, length):
        result += random.choice(base_string)

    return result
