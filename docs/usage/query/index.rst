.. _query-usage:

Query
=====

The :ref:`aiosnow.fields <fields-root>` classes provides a set of type-specific methods for creating queries.
Calling such a method returns a :class:`aiosnow.query.condition.Condition` with the string representation of a
ServiceNow sysparm.

Conditions can be chained using bitwise operators for AND, OR and XOR.

*Usage*

.. toctree::

   single
   list
   raw
