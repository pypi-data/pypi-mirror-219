- detect if test environment is active

.. include:: ../lib_detect_testenv/lib_detect_testenv.py
    :code: python
    :start-after: # is_testenv_active{{{
    :end-before:  # is_testenv_active}}}

- detect if doctest is active

.. include:: ../lib_detect_testenv/lib_detect_testenv.py
    :code: python
    :start-after: # is_doctest_active{{{
    :end-before:  # is_doctest_active}}}

- detect if pytest is active

.. include:: ../lib_detect_testenv/lib_detect_testenv.py
    :code: python
    :start-after: # is_pytest_active{{{
    :end-before:  # is_pytest_active}}}

- detect if setup.py is active

.. include:: ../lib_detect_testenv/lib_detect_testenv.py
    :code: python
    :start-after: # is_setup_active{{{
    :end-before:  # is_setup_active}}}

- detect if "setup.py test" is active

.. include:: ../lib_detect_testenv/lib_detect_testenv.py
    :code: python
    :start-after: # is_setup_test_active{{{
    :end-before:  # is_setup_test_active}}}

- add a path to the syspath

.. include:: ../lib_detect_testenv/lib_detect_testenv.py
    :code: python
    :start-after: # add_path_to_syspath{{{
    :end-before:  # add_path_to_syspath}}}

- put this in Your `__init__.py` to automatically add the package directory to the syspath if the test environment is active.
  This is useful for local testing of packages.

.. code-block:: python

    # __init__.py :
    # this should be Your first import in __init__
    from lib_detect_testenv import *
    if is_testenv_active():
        add_path_to_syspath(__file__)
