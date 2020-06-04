IntegerMap
----------

Converts nested mapping to a named tuple with id and query capabilities of type `Integer <#numeric>`_: (id <String>, string <String>)

.. note::

    This Field has `Integer <#numeric>`_ querying capabilities.

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
