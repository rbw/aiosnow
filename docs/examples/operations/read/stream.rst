Stream
======

*Example – Using the Snow stream-like for reading memory friendly chunks*

.. code-block:: python

    async with app.resource(Incident) as r:
        selection = select(
            Incident.number.starts_with("INC0039")
            | Incident.opened_at.after("2019-05-05 01:35:50")
        ).order_desc(Incident.number)

        async for item in r.stream(selection, limit=0, chunk_size=250):
            print(item)
