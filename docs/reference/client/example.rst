Example
-------

A simple :class:`aiosnow.Client` using *basic auth* for authentication.

.. code-block:: python

    import aiosnow

    client = aiosnow.Client(
        address="<instance-name>.service-now.com",
        basic_auth=("<username>", "<password>")
    )
