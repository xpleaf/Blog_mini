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

"""Generate random personal information."""

import random

from ..dictionaries_loader import get_dictionary

__all__ = ['gender', 'abbreviated_gender', 'shirt_size', 'race', 'language']


def gender():
    """Random gender."""
    return random.choice(get_dictionary('genders')).strip()


def abbreviated_gender():
    """Random abbreviated gender."""
    return gender()[0:1]


def shirt_size():
    """Shirt size."""
    return random.choice(get_dictionary('shirt_sizes')).strip()


def race():
    """Random race."""
    return random.choice(get_dictionary('races')).strip()


def language():
    """Random language name, e.g. ``Polish``."""
    return random.choice(get_dictionary('languages')).strip()
