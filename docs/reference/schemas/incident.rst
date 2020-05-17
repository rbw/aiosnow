Incident
========

Incident-type schemas modelled after ServiceNow table defaults.


Plain
-----

Returns *display_value* representation of related fields, such as state, impact, assignment_group etc.

.. automodule:: snow.schemas
   :members: IncidentPlain
   :undoc-members:
   :show-inheritance: false
   :exclude-members: snow_meta, opts

Mapped
------

Returns *display_name* representation of related fields, such as state, impact, assignment_group etc.

.. automodule:: snow.schemas
   :noindex:
   :members: IncidentMapped
   :undoc-members:
   :show-inheritance: false
   :exclude-members: snow_meta, opts

Expanded
--------

Resolves and deserializes nested fields such as assignment_group using the PartialSchema class.

.. automodule:: snow.schemas
   :noindex:
   :members: IncidentExpanded
   :undoc-members:
   :show-inheritance: false
   :exclude-members: snow_meta, opts

