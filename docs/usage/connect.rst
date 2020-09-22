Connect
-------

To connect to ServiceNow, a :class:`~aiosnow.Client` must be created.


.. code-block:: python

    import aiosnow

    client = aiosnow.Client(
        address="<instance-name>.service-now.com",
        basic_auth=("<username>", "<password>")
    )
