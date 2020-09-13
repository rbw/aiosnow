StringMap
---------

Converts nested mapping to a named tuple.

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

    Mapping(key="2", value="2 - Medium")


.. note::

    This field has querying powers of :ref:`String <fields-string>`: (id <String>, string <String>)
