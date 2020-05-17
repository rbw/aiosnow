.. _reference-fields:

Fields
======

Fields are used when defining :ref:`Resource Schemas <reference-schema>` and comes with type-specific query builders.

Text
----

.. automodule:: snow.resource.fields.text
   :members:
   

Numeric
-------

.. automodule:: snow.resource.fields.numeric
   :members:
   

Boolean
-------

.. automodule:: snow.resource.fields.boolean
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

.. automodule:: snow.resource.fields.datetime
   :members:
   


Choice
------

.. automodule:: snow.resource.fields.choice
   :members:
   


Email
-----

.. automodule:: snow.resource.fields.email
   :members:
   

Reference
---------

.. automodule:: snow.resource.fields.reference
   :members:
   

