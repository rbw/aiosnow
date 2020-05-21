Introduction
============

Snow is a simple and lightweight yet powerful and extensible library for interacting with ServiceNow. It works
with modern versions of Python, utilizes `asyncio <https://docs.python.org/3/library/asyncio.html>`_ and
can be used for simple scripting as well as for building high-concurrency backend applications on top of the ServiceNow platform.

For usage examples, visit `github.com/rbw/snow/examples <https://github.com/rbw/snow/examples>`_.


Requirements
------------

- Python 3.7+


Installation
------------

The library is available on PyPI and can be installed using pip.

.. code-block:: shell

   $ pip install snow


Dependencies
------------

Snow depends on a small set of stable and permissively licensed libraries.

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
   :titlesonly:
   :maxdepth: 3

   reference/snow
   reference/schema/index
   reference/model/index
   reference/response
   reference/exceptions

.. toctree::
   :caption: Other
   :maxdepth: 2

   other/config
   other/schemas/index
