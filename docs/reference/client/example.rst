Example
-------

A simple aiosnow application

.. code-block:: python

    from aiosnow import Client

    app = Client(
        "https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )
