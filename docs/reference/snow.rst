.. _ref-application:

Snow
====

The :class:`~snow.Snow` constructor takes a set of config parameters and provides an interface for
producing API Models and more.

API
---

.. automodule:: snow
   :members: Snow
   :exclude-members: get_session

Example
-------

A simple Snow application

.. code-block:: python

    from snow import Snow

    app = Snow(
        "https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )
