.. _fields-root:

Fields
======

Fields are used when defining a concrete Schema and comes with type-specific query builders.

They are used in:
    - Concrete Model definitions
    - Building and serializing queries
    - Request field selection
    - Request payload serialization
    - Response content deserialization

Text
----

.. automodule:: snow.model.schema.fields.text
   :members:
   

Numeric
-------

.. automodule:: snow.model.schema.fields.numeric
   :members:
   

Boolean
-------

.. automodule:: snow.model.schema.fields.boolean
   :members:
   


NumericMap
----------

Converts nested mapping to a named tuple with id and query capabilities of type `Numeric <#numeric>`_: (id <Text>, text <Text>)

.. note::

    This Field has `Numeric <#numeric>`_ querying capabilities.

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




Datetime
--------

.. automodule:: snow.model.schema.fields.datetime
   :members:
   


Choice
------

.. automodule:: snow.model.schema.fields.choice
   :members:
   


Email
-----

.. automodule:: snow.model.schema.fields.email
   :members:
