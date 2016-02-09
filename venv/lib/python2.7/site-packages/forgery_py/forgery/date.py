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

"""Generate random date-related data."""

import datetime
import random

from ..dictionaries_loader import get_dictionary

__all__ = ['day_of_week', 'month', 'year', 'day', 'date']

DAYS = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday',
    'Friday', 'Saturday', 'Sunday'
]

DAYS_ABBR = [
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'
]

MONTHS = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

MONTHS_ABBR = [
    'Jan', 'Feb', 'Mar', 'Apr',
    'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec'
]


def day_of_week(abbr=False):
    """Random (abbreviated if `abbr`) day of week name."""
    if abbr:
        return random.choice(DAYS_ABBR)
    else:
        return random.choice(DAYS)


def month(abbr=False, numerical=False):
    """
    Random (abbreviated if `abbr`) month name or month number if 
    `numerical`.
    """
    if numerical:
        return random.randint(1, 12)
    else:
        if abbr:
            return random.choice(MONTHS_ABBR)
        else:
            return random.choice(MONTHS)


def _delta(past=False, min_delta=0, max_delta=20):
    delta = min_delta + random.randint(min_delta + 1, max_delta)

    if past:
        delta = delta * -1

    return delta


def year(past=False, min_delta=0, max_delta=20):
    """Random year."""
    return datetime.date.today().year + _delta(past, min_delta, max_delta)


def day(month_length=31):
    """Random day number in a `month_length` days long month."""
    return random.randint(1, month_length)


def date(past=False, min_delta=0, max_delta=20):
    """Random `datetime.date` object. Delta args are days."""
    timedelta = datetime.timedelta(days=_delta(past, min_delta, max_delta))
    return datetime.date.today() + timedelta
