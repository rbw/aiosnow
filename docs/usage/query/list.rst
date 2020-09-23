.. _usage-query-list:

List
====

When querying for a list of items, :func:`aiosnow.select` with chained conditions can be used.

*Example*

.. code-block:: python

    query = aiosnow.select(
        Incident.number.starts_with("INC123")
        &
        Incident.impact.less_than(3)
        ^
        Incident.assignment_group.name.equals("Hardware")
    ).order_desc(Incident.number)

    async with Incident(client, table_name="incident") as inc:
        response = await inc.get(query, limit=10)
        print("The query yielded {} items.".format(len(response.data)))
