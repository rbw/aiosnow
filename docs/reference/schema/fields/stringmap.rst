StringMap
---------

Converts nested mapping to a named tuple with id and query capabilities of type :ref:`String <fields-string>`: (id <String>, string <String>)

.. note::

    This Field has :ref:`String <fields-string>` querying capabilities.

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
