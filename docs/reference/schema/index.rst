.. _ref-schema:

Schema
======

A Schema is defined using one or more :ref:`fields <fields-root>`. Concrete schemas typically also configures the *Model* it defines via the *Meta* inner class.
For instance, the *Meta.table_name* inner class attribute of a :class:`~aiosnow.models.table.TableSchema` would instruct the :class:`~aiosnow.models.table.TableModel`
to make use of the given *table name* when interacting with the *ServiceNow Table API*.

Check out the :ref:`builtin schemas <schemas-root>` if you're looking to get started quickly.


.. toctree::
   :titlesonly:
   :maxdepth: 2

   base
   fields/index
   partial
   builtins/index
