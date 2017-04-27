cSkipDict
=========

A fast, CFFI-based SkipDict implementation for Python.

``SkipDict`` instances are `Skip
List <https://en.wikipedia.org/wiki/Skip_list>`__-based associative
arrays ('dictionaries' in Python terms), mapping positive integers to
arbitrary Python objects. Keys are always stored and returned in order,
while maintaining average-case *O(log n)* search, insert and delete
times, and average-case space consumption of *O(n)*.

This libary uses Peter Cannici's public-domain
`skiplist.h <https://github.com/alpha123/skiplist.h>`__ C library,
adapting it slightly for use with Python and CFFI.

Installation
------------

Installation on most systems should be pretty easy:

::

        $ pip install cskipdict

Usage
-----

You can use it just like a normal ``dict``, except that all keys should
be positive integers less than 2\ :sup:`64`:

::

        >>> from cskipdict import SkipDict
        >>> d = SkipDict()
        >>> d
        SkipDict({})
        >>> len(d)
        0
        >>> d[123] = 'abc'
        >>> d
        SkipDict({123: 'abc'})
        >>> d[420] = 'def'
        >>> d
        SkipDict({123: 'abc', 420: 'def'})
        >>> d[69] = 'foo'
        >>> d
        SkipDict({69: 'foo', 123: 'abc', 420: 'def'})

Iteration will always happen in ascending order of the keys:

::

        >>> for k, v in d.iteritems():
        ...     print((k, v))
        (69, 'foo')
        (123, 'abc')
        (420, 'def')

Unlicense
---------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of
this software dedicate any and all copyright interest in the software to
the public domain. We make this dedication for the benefit of the public
at large and to the detriment of our heirs and successors. We intend
this dedication to be an overt act of relinquishment in perpetuity of
all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

For more information, please refer to http://unlicense.org/
