Application
===========

The :class:`snow.Application` expects a configuration dictionary and provides a factory for producing resources.

*Example – Simple Application*

.. code-block:: python

    from snow.resource import Application

    config = dict(
        address="https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )

    app = Application(config)


.. toctree::
    :hidden:

    model
    config
