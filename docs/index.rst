Introduction
============

Snow is a simple and lightweight yet powerful and extensible library for interacting with ServiceNow. It works
with modern versions of Python, utilizes `asyncio <https://docs.python.org/3/library/asyncio.html>`_ and
can be used for simple scripting as well as for building high-concurrency backend applications on top of the ServiceNow platform.


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
   :maxdepth: 3

   reference/application/index
   reference/resource/index
   reference/exceptions

.. toctree::
   :caption: Samples
   :maxdepth: 2

   samples/app
   samples/operations/index
