StringMap
---------

Converts nested mapping to a named tuple.

.. note::

    This field has querying powers of :ref:`String <fields-string>`: (id <String>, string <String>)

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
