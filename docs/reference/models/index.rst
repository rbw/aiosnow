.. _ref-model:

Models
======

To perform ServiceNow API operations, a *Model* object must first be created. This is done via either a :class:`~aiosnow.Client` factory
method, or by importing and instantiating the desired concrete *Model* directly.

Concrete builtin Models, such as those of :class:`~aiosnow.models.table.TableModel` type, are modelled after default ServiceNow API resources.


.. toctree::
   :titlesonly:

   base
   table/index
