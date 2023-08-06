=========
 Changes
=========

2.0 (2023-07-18)
================

- Drop support for Python 2.7, 3.5, 3.6.

- Add support for Python 3.9, 3.10, 3.11.


1.1 (2019-06-10)
================

- Claim support of Python 3.5, 3.6, 3.7, 3.8, PyPy and PyPy3.

- Use tox for testing.


1.0 (2016-04-06)
================

- Update `bootstrap.py` to a ``zc.buildout 2.3``.

- Use py.test as test runner.

- Declare the explicit support of Python 2.7.
  No other Python versions are currently supported.

0.4 (2013-03-28)
================

- When registering a pagelet using ZCML which only has template, the name of
  the template is rendered in the ``repr`` the generated class to have a
  clue what is the purpose of this class when debugging.

- Updated tests to use Python's `doctest` instead of deprecated
  `zope.testing.doctest`.


0.3 (2009-12-27)
================

- Using ``zope.browserpage`` and ``zope.browsermenu`` instead of
  ``zope.app.publisher``.


0.2 (2009-12-27)
================

- Allow arbitrary number of context elements for adaptation.

0.1 (2008-09-20)
================

- First public release.


==============
 Contributors
==============

- Michael Howitz <mh at gocept dot com>

- Christian Theune <ct at gocept dot com>
