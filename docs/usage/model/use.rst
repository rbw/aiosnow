Use
---

A declared Model can be instantiated for reading and altering data in ServiceNow.

*Example*

.. code-block:: python

    async with Incident(client, table_name="incident") as inc:
        response = await inc.get_one(Incident.number == "INC0000001")
        print(response.data)
