Single
======

Single conditions are typically used when updating, deleting or fetching a specific item by a unique identifier.

*Example*

.. code-block:: python

    response = await inc.update(
        Incident.number == "INC0000001",
        dict(
            description="Hello!"
        )
    )
    print("Updated description => {description}".format(**response.data))
