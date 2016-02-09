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

"""Generate random `Lorem ipsum` style text."""

import random
import re

from ..dictionaries_loader import get_dictionary

__all__ = [
    'word', 'words', 'title', 'sentence',
    'sentences', 'paragraph', 'paragraphs'
]

_words = None


def word():
    """Random word."""
    return words(quantity=1)


def words(quantity=10, as_list=False):
    """Random words."""
    global _words

    if not _words:
        _words = ' '.join(get_dictionary('lorem_ipsum')).lower().\
            replace('\n', '')
        _words = re.sub(r'\.|,|;/', '', _words)
        _words = _words.split(' ')

    result = random.sample(_words, quantity)

    if as_list:
        return result
    else:
        return ' '.join(result)


def title(words_quantity=4):
    """Random sentence to be used as e.g. an e-mail subject."""
    result = words(quantity=words_quantity)
    result += random.choice('?.!')
    return result.capitalize()


def sentence():
    """Random sentence."""
    return sentences(quantity=1)


def sentences(quantity=2, as_list=False):
    """Random sentences."""
    result = [sntc.strip() for sntc in
              random.sample(get_dictionary('lorem_ipsum'), quantity)]

    if as_list:
        return result
    else:
        return ' '.join(result)


def paragraph(separator='\n\n', wrap_start='', wrap_end='',
              html=False, sentences_quantity=3):
    """Random paragraph."""
    return paragraphs(quantity=1, separator=separator, wrap_start=wrap_start,
                      wrap_end=wrap_end, html=html,
                      sentences_quantity=sentences_quantity)


def paragraphs(quantity=2, separator='\n\n', wrap_start='', wrap_end='',
               html=False, sentences_quantity=3, as_list=False):
    """Random paragraphs."""
    if html:
        wrap_start = '<p>'
        wrap_end = '</p>'
        separator = '\n\n'

    result = []
    for i in xrange(0, quantity):
        result.append(wrap_start + sentences(sentences_quantity) + wrap_end)

    if as_list:
        return result
    else:
        return separator.join(result)
