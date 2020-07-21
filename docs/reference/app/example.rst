Example
-------

A simple Snow application

.. code-block:: python

    from aiosnow import Snow

    app = Snow(
        "https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )
