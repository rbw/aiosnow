# snow: Python asyncio library for ServiceNow

[![image](https://badgen.net/pypi/v/snow)](https://pypi.org/project/snow)
[![image](https://badgen.net/badge/python/3.7+?color=purple)](https://pypi.org/project/snow)
[![image](https://badgen.net/travis/rbw/snow)](https://travis-ci.org/rbw/snow)
[![image](https://badgen.net/pypi/license/snow)](https://raw.githubusercontent.com/rbw/snow/master/LICENSE)
[![image](https://pepy.tech/badge/snow/month)](https://pepy.tech/project/snow)


Snow is a simple and lightweight yet powerful and extensible library for interacting with ServiceNow. It works
with modern versions of Python, utilizes [asyncio](https://docs.python.org/3/library/asyncio.html) and
can be used for simple scripting as well as for building high-concurrency backend applications on top of the ServiceNow platform.
Also, its API is fully type annotated and documented.

*Example code*
```python

import asyncio

from snow import Snow
from snow.schemas.table import IncidentSchema as Incident

app = Snow("<instance>.service-now.com", basic_auth=("<username>", "<password>"))

async def main():
    # Make a TableModel object from the built-in Incident schema
    async with app.get_table(Incident) as inc:
        # Get high-priority incidents
        for response in await inc.get(Incident.priority <= 3, limit=5):
            print(f"Number: {response['number']}, Priority: {response['priority'].text}")

asyncio.run(main())

```

Check out the [examples directory](examples) for more examples.

Documentation
---

The Snow API reference and more is available in the [documentation](https://python-snow.readthedocs.io/en/latest).


Funding
-------

The Snow code is permissively licensed, and can be incorporated into any type of application–commercial or otherwise–without costs or limitations.
Its author believes it's in the commercial best-interest for users of the project to invest in its ongoing development.

Consider leaving a [donation](https://paypal.vault13.org) if you like this software, it will:

- Directly contribute to faster releases, more features, and higher quality software.
- Allow more time to be invested in documentation, issue triage, and community support.
- Safeguard the future development of Snow.

Development status
---

The fundamental components (models, client code, error handling, documentation, etc) of the library is considered complete.
However, automatic testing and real-world use is somewhat lacking, i.e. there are most likely bugs lurking about,
and the software should be considered Alpha, shortly Beta.

Contributing
---

Check out the [contributing guidelines](CONTRIBUTING.md) if you want to help out with code or documentation.


Author
------

Robert Wikman \<rbw@vault13.org\>

