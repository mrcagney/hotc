Heart of the City
******************
A Python 3.6+ library to issue asynchronous GET requests to the Heart of the City API to get walking counts for center city Auckland, New Zealand.
The API has access to counts from 2012-01-23 to the present.


Installation
=============
``poetry add --git https://github.com/mrcagney/hotc hotc``


Usage
======
See the Jupyter notebook ``ipynb/examples.ipynb``.


Notes
======
- Development status is Alpha
- This project uses semantic versioning
- Need to add more documentation and tests


Authors
========
- Alex Raichev (2017-11-17)


Changes
========

2.0.0, 2019-10-11
-----------------
- Switched back to vanilla requests, because requests-futures wasn't faster.
- Breaking change: simplified get_hotc to make one request.


1.0.3, 2019-01-14
-----------------
- Switched to Poetry.
- Fixed ``requests-futures`` deprecation warnings.


1.0.2, 2018-11-07
-----------------
- Updated API URL.


1.0.1, 2018-02-26
-----------------
- Fixed error in case of empty HTTP 200 response.
- Corrected version number.


0.0.0, 2017-11-17
-------------------
- First release.
