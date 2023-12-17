Heart of the City
******************
A Python 3.9+ library to call the Heart of the City API to get walking counts for center city Auckland, New Zealand.
The API has access to counts from 2012-01-23 to the present.


Installation
=============
``poetry add --git https://github.com/mrcagney/hotc``


Usage
======
See the Jupyter notebook ``notebooks/examples.ipynb``.


Notes
======
- Development status is Alpha
- This project uses semantic versioning
- Need to add more documentation and tests


Authors
========
- Alex Raichev (maintainer), 2017-11-17


Changelog
=========

3.1.0, 2023-12-18
-----------------
- Updated counter locations to agree with `the current ones Heart of the City publishes <https://www.hotcity.co.nz/sites/20180201.prod.hotcity.co.nz/files/2022-08/Pedestrian%20Geodata%20%28Mitchell%20update%29.xlsx>`_.
- Updated dependencies.

3.0.0, 2023-07-05
-----------------
- Changed fields to 'counter_id' and 'counter_name'.
- Updated counter names to agree with those returned by the API.
- Improved docstrings.

2.2.1, 2023-07-04
-----------------
- Bugfixed date formatting and boolean inpurt errors introduced in version 2.2.0.

2.2.0, 2023-07-04
-----------------
- Updated dependencies.
- Updated walking counters.
- Added type hints.

2.1.1, 2022-01-20
-----------------
- Uncapped dependency versions.


2.1.0, 2021-08-09
-----------------
- Upgraded to Python 3.9.


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
