.. _resource:

Resource
========

To perform API operations, a :class:`~snow.resource.Resource` model must be created, this is done
by passing a :class:`~snow.resource.schema.Schema` to the :meth:`snow.Application.resource` factory.

.. code-block:: python

    import snow
    from snow.schemas import IncidentSimple as Incident

    app = snow.Application(
        "https://my-instance.service-now.com",
        basic_auth=("<username>", "<password>")
    )

    # Create new Resource model using the built-in Incident schema
    async with app.resource(Incident) as r:
        # Get incident with number INC01234
        response = await r.get_one(Incident.number == "INC01234")
        print(response["description"])

**Contents**

.. toctree::
   :maxdepth: 1

   schema
   model
