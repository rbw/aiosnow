.. _schemas-root:

Builtin
=======

At some point you probably want to roll your *own* schemas, however, if you're looking to get started quickly,
the built-in `aiosnow.schemas` package is the speedy route. It contains :class:`~aiosnow.models.common.schema.base.BaseSchema`
type classes modelled after the ServiceNow table defaults, and can be used either directly or tailored to your needs.

Consider sharing common ServiceNow tables schemas at: `github.com/rbw/aiosnow/pulls <https://github.com/rbw/aiosnow/pulls>`_

.. toctree::
   :maxdepth: 2

   table/index
