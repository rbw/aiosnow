# aiosnow: Asynchronous Python ServiceNow library

[![image](https://badgen.net/pypi/v/aiosnow)](https://pypi.org/project/aiosnow)
[![image](https://badgen.net/badge/python/3.7+?color=purple)](https://pypi.org/project/aiosnow)
[![image](https://badgen.net/travis/rbw/aiosnow)](https://travis-ci.org/rbw/aiosnow)
[![image](https://badgen.net/pypi/license/aiosnow)](https://raw.githubusercontent.com/rbw/aiosnow/master/LICENSE)
[![image](https://pepy.tech/badge/snow/month)](https://pepy.tech/project/snow)

The aiosnow library is a simple, lightweight and extensible tool for interacting with ServiceNow.
It utilizes [asyncio](https://docs.python.org/3/library/asyncio.html) and especially shines when building high-concurrency backend applications on top of the ServiceNow platform, but can be used for scripting as well.

*Example code*
```python
import asyncio
import aiosnow
from aiosnow.schemas.table import IncidentSchema as Incident

snow = aiosnow.Client("<instance>.service-now.com", basic_auth=("<username>", "<password>"))

async def main():
    # Make a TableModel object for interacting with the table API
    async with snow.get_table(Incident) as inc:
        # Fetch high-priority incidents
        for response in await inc.get(Incident.priority <= 3, limit=5):
            print(f"Number: {response['number']}, Priority: {response['priority'].text}")

asyncio.run(main())
```

Check out the [examples directory](examples) for more.

### Documentation

The aiosnow reference and more is available in the [documentation](https://aiosnow.readthedocs.io/en/latest).


### Funding

The aiosnow code is permissively licensed, and can be incorporated into any type of application–commercial or otherwise–without costs or limitations.
Its author believes it's in the commercial best-interest for users of the project to invest in its ongoing development.

Consider leaving a [donation](https://paypal.vault13.org) if you like this software, it will:

- Directly contribute to faster releases, more features, and higher quality software.
- Allow more time to be invested in documentation, issue triage, and community support.
- Safeguard the future development of aiosnow.

### Development status

The fundamental components (models, client code, error handling, documentation, etc) of the library is considered complete.
However, automatic testing and real-world use is somewhat lacking, i.e. there are most likely bugs lurking about,
and the software should be considered Alpha, shortly Beta.

### Contributing

Check out the [contributing guidelines](CONTRIBUTING.md) if you want to help out with code or documentation.


### Author

Robert Wikman \<rbw@vault13.org\>

