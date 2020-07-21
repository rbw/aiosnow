.. _config:

Config
======

The :class:`~aiosnow.Snow` class constructor takes a set of configuration parameters which are deserialized into
an object in the :data:`~aiosnow.Snow.config` attribute.


*Snow configuration options*


========== ======== ======= ============= ===========================
Name       Required Default Type          Description
========== ======== ======= ============= ===========================
address    True     None    String        Instance TCP address
basic_auth False    None    Tuple         Basic auth credentials
use_ssl    True     True    Boolean       Whether to use SSL
verify_ssl True     True    Boolean       Verify SSL certificates
session    False    None    ClientSession Custom ClientSession object
========== ======== ======= ============= ===========================

.. note::

    Custom sessions' `response_class` must be set to :class:`aiosnow.request.response.Response` for it to be compatible with Snow.
