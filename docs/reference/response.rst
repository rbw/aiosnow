Response
========

Concrete Models' API methods, such as :meth:`~aiosnow.models.table.TableModel.get_one` of :class:`~aiosnow.models.table.TableModel`,
returns this object as response to HTTP requests.

Some facts about this object:

- Iterating over a Response yields items from Response.data
- Accessing a Response as a dict returns the requested item from Response.data
- Its object representation is a response overview


API
---

.. automodule:: aiosnow.request.response
   :members: Response
   :exclude-members: load
