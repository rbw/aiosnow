Single
======

Single conditions are typically used when updating, deleting or fetching a specific item by a unique identifier.

*Example*

.. code-block:: python

    async with Incident(client, table_name="incident") as inc:
        response = await inc.update(
            Incident.number == "INC0000001",
            dict(
                description="Hello!"
            )
        )
        print("Updated description: {}".format(response["description"]))
