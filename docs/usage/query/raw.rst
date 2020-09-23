Raw
===

Shows how a sysparm query string can be passed directly to a query method.
See the :class:`~aiosnow.query.condition.Condition` equivalent :ref:`here <usage-query-list>`.

.. code-block:: python

    async with Incident(client, table_name="incident") as inc:
        response = await inc.get(
            "numberSTARTSWITHINC00000^impact<3^ORDERBYDESCnumber"
        )
        print("The query yielded {} items.".format(len(response.data)))
