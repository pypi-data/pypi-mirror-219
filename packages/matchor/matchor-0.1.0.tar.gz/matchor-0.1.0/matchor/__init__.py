#
# MIT License
#
# Copyright (c) 2023 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Extended Pattern Matching.
"""


import functools
import re


@functools.lru_cache()
def _compile_pattern(pat):
    res = _translate(pat)
    return re.compile(res).match


def _translate(pat):
    res = ["(?ms)"]
    for item in pat:
        if item == "*":
            res.append(".*")
        elif item == "?":
            res.append(".")
        else:
            res.append(re.escape(item))
    res.append(r"\Z")
    return "".join(res)


def is_pattern(pattern):
    """Return `True` if `pattern` contains `*` or `?`."""
    return "*" in pattern or "?" in pattern


def match(name, pattern):
    """
    Return `True` if `name` matches `pattern`.

    Pattern may contain `*` and `?`. `*` matches any characters, `?` matches exactly one character.

    >>> match('foo', 'foo')
    True
    >>> match('foo', '*')
    True
    >>> match('foo', 'bar*')
    False
    >>> match('foo', 'fo?')
    True
    """
    if pattern == "*":
        return True
    if is_pattern(pattern):
        func = _compile_pattern(pattern)
        return func(name) is not None
    return name == pattern


def matchs(name, patterns) -> bool:
    """
    Return `True` if `name` matches element of `patterns`.

    Pattern may contain `*` and `?`. `*` matches any characters, `?` matches exactly one character.

    >>> matchs('foo', ['foo', 'bar'])
    True
    >>> matchs('foo', ['*'])
    True
    >>> matchs('foo', ['bar*', 'baz'])
    False
    >>> matchs('ba', ['bar*', 'baz'])
    False
    >>> matchs('baz', ['bar*', 'baz'])
    True
    >>> matchs('baz2', ['bar*', 'baz'])
    False
    """
    for pattern in patterns:
        if match(name, pattern):
            return True
    return False


def matchsp(name, patterns):
    """
    Return matching pattern if `name` matches element of `patterns`.

    Pattern may contain `*` and `?`. `*` matches any characters, `?` matches exactly one character.

    >>> matchsp('foo', ['foo', 'bar'])
    'foo'
    >>> matchsp('foo', ['*'])
    '*'
    >>> matchsp('foo', ['bar*', 'baz'])
    >>> matchsp('ba', ['bar*', 'baz'])
    >>> matchsp('baz', ['bar*', 'baz'])
    'baz'
    >>> matchsp('baz2', ['bar*', 'baz'])
    """
    for pattern in patterns:
        if match(name, pattern):
            return pattern
    return None
