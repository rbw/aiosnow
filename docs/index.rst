Introduction
============

The aiosnow library is a simple, lightweight and extensible tool for interacting with ServiceNow. It utilizes asyncio and especially shines when building high-concurrency backend applications on top of the ServiceNow platform, but can be used for scripting as well.

For usage examples, please visit `github.com/rbw/aiosnow/examples <https://github.com/rbw/aiosnow/tree/master/examples>`_.


Requirements
------------

- Python 3.7+


Installation
------------

The library is available on PyPI and can be installed using pip.

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

   reference/client/index
   reference/schema/index
   reference/models/index
   reference/response
   reference/exceptions

.. toctree::
   :caption: Other
   :maxdepth: 2

   other/config
   other/schemas/index
