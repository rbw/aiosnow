.. _app-sample:

Application
===========

At the core of Snow lies :class:`snow.Application`, which expects a configuration dictionary that conforms to the :ref:`Application Configuration Schema <config>`.
Once created, an interface for producing :class:`~snow.resource.Resource` models is provided.

*Application Sample*

.. code-block:: python

    from snow import Application

    config = dict(
        address="https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )

    app = Application(config)

    async with app.resource(Incident) as r:
        [do stuff]
