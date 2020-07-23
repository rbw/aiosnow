.. _ref-model:

Models
======

To perform API operations, a Model object must first be created. This is done either via a :class:`~aiosnow.Client` factory
method, or by importing and instantiating the desired concrete Model directly.

Concrete built-in Models, such as those of :class:`~aiosnow.models.TableModel` type, are modelled after default ServiceNow API resources.


.. toctree::
   :titlesonly:

   base
   table/index
