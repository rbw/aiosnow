.. _config:

Config
======

The :class:`snow.Application` takes a config argument; once validated and transformed, the end result is a configuration object in :data:`snow.Application.config`.


.. rubric:: Schema


The Config Schema is used for validation and transformation of the input configuration that was passed to a :class:`snow.Application`.

.. automodule:: snow.config
   :members: ConfigSchema
   :exclude-members: opts, OPTIONS_CLASS, post_load, InternalConfig
