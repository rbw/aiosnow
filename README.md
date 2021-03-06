# aiosnow: Asynchronous Python ServiceNow Library

[![image](https://badgen.net/pypi/v/aiosnow)](https://pypi.org/project/aiosnow)
[![image](https://badgen.net/badge/python/3.7+?color=purple)](https://pypi.org/project/aiosnow)
[![image](https://badgen.net/travis/rbw/aiosnow)](https://travis-ci.org/rbw/aiosnow)
[![image](https://badgen.net/pypi/license/aiosnow)](https://raw.githubusercontent.com/rbw/aiosnow/master/LICENSE)
[![image](https://pepy.tech/badge/snow/month)](https://pepy.tech/project/snow)

**aiosnow** is a Python [asyncio](https://docs.python.org/3/library/asyncio.html) library for interacting with ServiceNow programmatically. It hopes to be:

- Convenient: A good deal of work is put into making the library flexible and easy to use.
- Performant: Uses non-blocking I/O to allow large amounts of API request tasks to run concurrently while being friendly on system resources.
- Modular: Core functionality is componentized into modules that are built with composability and extensibility in mind.

*Example code*

```python
import asyncio

import aiosnow
from aiosnow.models.table.declared import IncidentModel as Incident

async def main():
    client = aiosnow.Client("<instance>.service-now.com", basic_auth=("<username>", "<password>"))

    async with Incident(client, table_name="incident") as inc:
        query = aiosnow.select(
            Incident.priority.less_or_equals(2) & Incident.urgency.less_or_equals(2)
        ).order_asc(Incident.priority)

        for response in await inc.get(query, limit=5):
            print("Attaching [readme.txt] to {number} ({sys_id})".format(**response))
            await inc.upload_file(response["sys_id"], path="./readme.txt")

asyncio.run(main())
```

Check out the [examples directory](examples) for more material.

### Documentation

API reference and more is available in the [technical documentation](https://aiosnow.readthedocs.io/en/latest).


### Development status

Beta: Core functionality is done and API breakage unlikely to happen.


### Contributing

Check out the [contributing guidelines](CONTRIBUTING.md) if you want to help out with code or documentation.


### Author

Robert Wikman \<rbw@vault13.org\>

