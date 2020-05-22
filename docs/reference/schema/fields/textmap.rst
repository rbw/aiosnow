TextMap
-------

Converts nested mapping to a named tuple with id and query capabilities of type `Text <#text>`_: (id <Text>, text <Text>)

.. note::

    This Field has `Text <#text>`_ querying capabilities.

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
