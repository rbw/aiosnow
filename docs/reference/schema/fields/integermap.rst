IntegerMap
----------

Converts nested mapping to a named tuple with id and query capabilities of type :ref:`Integer <fields-integer>`: (id <Integer>, string <String>)

.. note::

    This Field has :ref:`Integer <fields-integer>` querying capabilities.

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

    Mapping(id=2, text="2 - Medium")
