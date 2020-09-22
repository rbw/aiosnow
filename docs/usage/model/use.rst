Use
---

Declared Models can be instantiated and used to read and manipulate data in ServiceNow.

.. code-block:: python

    async with Incident(client, table_name="incident") as inc:
        response = await inc.get_one(Incident.number == "INC0000001")
        print(response.data)
