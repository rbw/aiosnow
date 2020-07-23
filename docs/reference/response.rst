Response
========

Concrete Models' API methods, such as :meth:`~aiosnow.models.table.TableModel.get_one` of :class:`~aiosnow.models.table.TableModel`,
returns an instance of this class as response to HTTP requests.

Some facts about this object:

- Iterating over a Response yields from Response.data
- When accessed as a dict, the requested item from Response.data is returned
- Its representation is a response overview


API
---

.. automodule:: aiosnow.request.response
   :members: Response
   :exclude-members: load
