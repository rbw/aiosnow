StringMap
---------

Converts nested mapping to a named tuple with id and query capabilities of type `String <#string>`_: (id <String>, string <String>)

.. note::

    This Field has `String <#string>`_ querying capabilities.

Response content of:

.. code-block:: json

    {
       "impact":{
          "value":2,
          "display_value":"2 - Medium"
       }
    }

Gets deserialized into:

.. code-block:: python

    Mapping(id="2", text="2 - Medium")
