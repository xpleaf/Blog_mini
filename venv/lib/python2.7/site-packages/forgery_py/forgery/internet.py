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

import random

from ..dictionaries_loader import get_dictionary
from .name import first_name

__all__ = [
    'user_name', 'top_level_domain', 'domain_name',
    'email_address', 'cctld', 'ip_v4'
]


def user_name(with_num=False):
    """
    Random user name.

    Basically it's lowercased result of 
    :py:func:`~forgery_py.forgery.name.first_name()` with a number appended 
    if `with_num`.
    """
    result = first_name()
    if with_num:
        result += str(random.randint(63, 94))

    return result.lower()


def top_level_domain():
    """Random TLD."""
    return random.choice(get_dictionary('top_level_domains')).strip()


def domain_name():
    """
    Random domain name.

    Lowercased result of :py:func:`~forgery_py.forgery.name.company_name()` 
    plus :py:func:`~top_level_domain()`.
    """
    result = random.choice(get_dictionary('company_names')).strip()
    result += '.' + top_level_domain()

    return result.lower()


def email_address(user=None):
    """
    Random e-mail address in a hopefully imaginary domain.

    If `user` is ``None`` :py:func:`~user_name()` will be used. Otherwise it 
    will be lowercased and will have spaces replaced with ``_``.

    Domain name is created using :py:func:`~domain_name()`.
    """
    if not user:
        user = user_name()
    else:
        user = user.strip().replace(' ', '_').lower()

    return user + '@' + domain_name()


def cctld():
    """Random country code TLD."""
    return random.choice(get_dictionary('country_code_top_level_domains')).\
        strip()


def ip_v4():
    """Random IPv4 address."""
    return '.'.join([str(random.randint(0, 255)) for i in xrange(0, 4)])
