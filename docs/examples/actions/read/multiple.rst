Multiple
========

.. code-block:: python

    async with app.resource(Incident) as r:
        selection = select(
            Incident.number.starts_with("INC0039")
            | Incident.opened_at.after("2019-05-05 01:35:50")
        ).order_desc(Incident.number)

        for record in await r.get(limit=50):
            print(record["sys_id"])
