Single
======

*Example – Fetching of exactly one record*

.. code-block:: python

    async with app.resource(Incident) as r:
        selection = Incident.number.equals("INC0010049")
        record = await r.get_one(selection)
        print(record)
