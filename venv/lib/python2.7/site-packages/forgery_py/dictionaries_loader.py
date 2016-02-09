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

"""File-based dictionaries support."""

import codecs
from os.path import abspath, dirname, join
import random

DICTIONARIES_PATH = abspath(join(dirname(__file__), 'dictionaries'))

dictionaries_cache = {}


def get_dictionary(dict_name):
    """
    Load a dictionary file ``dict_name`` (if it's not cached) and return its
    contents as an array of strings.
    """
    global dictionaries_cache

    if dict_name not in dictionaries_cache:
        try:
            dictionary_file = codecs.open(
                join(DICTIONARIES_PATH, dict_name), 'r', 'utf-8'
            )
        except IOError:
            None
        else:
            dictionaries_cache[dict_name] = dictionary_file.readlines()
            dictionary_file.close()

    return dictionaries_cache[dict_name]
