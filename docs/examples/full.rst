All-inclusive
=============

The purpose of this example is to demonstrate how an actual script, rather than just a segment, can be written to:

- Create an event loop for running the `main()` coroutine
- Define a Resource Schema
- Use common Snow CRUD operations


*Full example – Schema definition, invocation, operations*

.. code-block:: python

    import asyncio

    from snow.resource import Schema, fields
    from snow import Application, Joined, select


    class Incident(Schema):
        __location__ = "/api/now/table/incident"

        sys_id = fields.Text(is_primary=True)
        number = fields.Text()
        description = fields.Text()
        short_description = fields.Text()
        impact = fields.Numeric()
        assignment_group = fields.Text(pluck=Joined.DISPLAY_VALUE)
        opened_at = fields.Datetime()


    async def main():
        app = Application(
            dict(
                address="https://<instance_name>.service-now.com",
                basic_auth=("<username>", "<password>")
            )
        )

        async with app.resource(Incident) as r:
            created = await r.create({
                Incident.short_description: "Test incident",
                Incident.description: "This is just a test.",
            })

            print(f"[>>>] Created: {created}")

            updated = await r.update(
                created["sys_id"],
                {
                    Incident.description: "Still just a test",
                    Incident.impact: 2,
                }
            )

            print(f"[>>>] Updated: {updated}")

            selection = select(
                Incident.impact.equals(updated["impact"]) &
                Incident.opened_at.after("2020-01-01")
            ).order_desc(Incident.number)

            print(
                f"[>>>] Fetching last 5 records with the same impact "
                f"as {updated['number']}, created after 2020-01-01..."
            )

            async for record in r.stream(selection, limit=5):
                print(record)

            print(f"[>>>] Cleaning up...")

            result = await r.delete(created["sys_id"])

            print(result)


    if __name__ == "__main__":
        asyncio.run(main())
