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

"""Generate random names and name-related strings."""

import random

from ..dictionaries_loader import get_dictionary

__all__ = [
    'first_name', 'last_name', 'full_name', 'male_first_name',
    'female_first_name', 'company_name', 'job_title', 'job_title_suffix',
    'title', 'suffix', 'location', 'industry'
]


def first_name():
    """Random male of female first name."""
    _dict = get_dictionary('male_first_names')
    _dict += get_dictionary('female_first_names')

    return random.choice(_dict).strip()


def last_name():
    """Random last name."""
    return random.choice(get_dictionary('last_names')).strip()


def full_name():
    """
    Random full name. Equivalent of ``first_name() + ' ' + last_name()``.
    """
    return first_name() + ' ' + last_name()


def male_first_name():
    """Random male first name."""
    return random.choice(get_dictionary('male_first_names')).strip()


def female_first_name():
    """Random female first name."""
    return random.choice(get_dictionary('female_first_names')).strip()


def company_name():
    """Random company name."""
    return random.choice(get_dictionary('company_names')).strip()


def job_title():
    """Random job title."""
    result = random.choice(get_dictionary('job_titles')).strip()
    result = result.replace('#{N}', job_title_suffix())
    return result


def job_title_suffix():
    """Random job title suffix."""
    return random.choice(get_dictionary('job_title_suffixes')).strip()


def title():
    """Random name title, e.g. ``Mr``."""
    return random.choice(get_dictionary('name_titles')).strip()


def suffix():
    """Random name suffix, e.g. ``Jr``."""
    return random.choice(get_dictionary('name_suffixes')).strip()


def location():
    """Random location name, e.g. ``MI6 Headquarters``."""
    return random.choice(get_dictionary('locations')).strip()


def industry():
    """Random industry name."""
    return random.choice(get_dictionary('industries')).strip()
