.. _config:

Config
======

The :class:`aiosnow.Client` constructor accepts a number of configuration parameters.

*aiosnow configuration parameters*


========== ======== ======= ============= ===========================
Name       Required Default Type          Description
========== ======== ======= ============= ===========================
address    True     None    String        Instance TCP address
basic_auth False    None    Tuple         Basic auth credentials
use_ssl    True     True    Boolean       Whether to use SSL
verify_ssl True     True    Boolean       Verify SSL certificates
session    False    None    ClientSession Custom ClientSession object
========== ======== ======= ============= ===========================
