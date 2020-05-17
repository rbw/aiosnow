.. _config:

Config
======

The :class:`snow.Application` takes a set of configuration parameters, once validated and transformed, the end result is a configuration object in :data:`snow.Application.config`.


*Snow Application configuration options*


========== ======== ======= ============= ===========================
Name       Required Default Type          Description
========== ======== ======= ============= ===========================
address    True     None    String        Instance TCP address
basic_auth False    None    Tuple         Basic auth credentials
use_ssl    True     True    Boolean       Whether to use SSL
verify_ssl True     True    Boolean       Verify SSL certificates
session    False    None    ClientSession Custom ClientSession object
========== ======== ======= ============= ===========================
