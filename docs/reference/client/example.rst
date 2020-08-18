Example
-------

A simple **aiosnow** application.

.. code-block:: python

    import aiosnow

    snow = aiosnow.Client(
        address="<instance-name>.service-now.com",
        basic_auth=("<username>", "<password>")
    )
