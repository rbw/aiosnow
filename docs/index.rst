Introduction
============

Snowstorm is a simple and lightweight yet powerful library for interacting with ServiceNow. It works
with modern versions of Python and utilizes `asyncio <https://docs.python.org/3/library/asyncio.html>`_.

Requirements
------------

- Python 3.7+


Installation
------------

Snowstorm is on PyPI and can be installed using pip.

.. code-block:: shell

   $ pip install snowstorm


Dependencies
------------

Snowstorm depends on a small set of stable and permissively licensed libraries.


- `aiohttp <https://github.com/aio-libs/aiohttp>`_: Communication
- `marshmallow <https://marshmallow.readthedocs.io/en/stable>`_: Schema system
- `ultrajson <https://github.com/esnme/ultrajson>`_: JSON encoder and decoder

Table of Contents
-----------------

.. toctree::
   :maxdepth: 1
   :hidden:

   self
   funding

.. toctree::
   :caption: Reference

   reference/client

.. toctree::
   :caption: Examples
   :maxdepth: 1

   examples/create/index
