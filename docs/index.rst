About
=====

**aiosnow** is a Python `asyncio <https://docs.python.org/3/library/asyncio.html>`_ library for interacting with ServiceNow programmatically. It hopes to be:

- Convenient: A good deal of work is put into making the library flexible and easy to use.
- Performant: Remote API calls uses non-blocking sockets tracked by an event loop, allowing large amounts of lightweight request tasks to run concurrently.
- Modular: Core functionality is componentized into modules that are built with composability and extensibility in mind.

For usage examples, visit `github.com/rbw/aiosnow/examples <https://github.com/rbw/aiosnow/tree/master/examples>`_.


Requirements
------------

- Python 3.7+


Installation
------------

The library is available on PyPI and can be installed using **pip**.

.. code-block:: shell

   $ pip install aiosnow


Dependencies
------------

The aiosnow library depends on a small set of stable and permissively licensed libraries.

- `aiohttp <https://github.com/aio-libs/aiohttp>`_: Communication
- `marshmallow <https://marshmallow.readthedocs.io/en/stable>`_: Schema system

Table of Contents
-----------------

.. toctree::
   :maxdepth: 1
   :hidden:

   self
   funding

.. toctree::
   :caption: Reference
   :maxdepth: 3
   :titlesonly:

   reference/client
   reference/models/index
   reference/fields/index
   reference/condition
   reference/response
   reference/exceptions

.. toctree::
   :caption: Usage
   :maxdepth: 2

   usage/connect
   usage/model/index
   usage/query/index
