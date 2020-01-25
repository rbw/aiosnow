Application
===========

The :class:`snow.Application` functions as an entry point for the Snow library.
Given a configuration, it provides a factory for producing :class:`~snow.resource.Resource` objects.

*Example – Simple Application*

.. code-block:: python

    from snow.resource import Application

    config = dict(
        address="https://my-instance.service-now.com",
        basic_auth=("my_user", "my_password")
    )

    snow = Application(config)

**Contents**

.. toctree::

    interface
    config/index
