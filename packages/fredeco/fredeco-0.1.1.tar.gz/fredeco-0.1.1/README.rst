=============
Description
=============

This python package allows its users to retrieve economic data provided by FRED® API. Although ``fredeco`` uses FRED® API, it is not endorsed or certified by the Federal Reserve Bank of St. Louis. 

===========
Features
===========

* Retrieve a time series, when indicating the ID of the related indicator;
* Retrieve several time series, indicating their IDs;
* Search for all indicators related to the keywords indicated by the user;
* Find all indicators of a category of series, by indicating the ID of the category;
* Find the dates of all release of an indicator;
* Find the information related to an indicator, such as the notes where the source of data can be found.

================
Installation
================


    $ pip install fredeco


===============
Dependencies
===============
* `pandas <https://pandas.pydata.org/>`_
* `numpy <https://numpy.org/>`_
* `requests <https://requests.readthedocs.io/en/latest/>`_
* `datetime <https://docs.python.org/3/library/datetime.html>`_


=========
Usage
=========
The usage of the package is explained in this section, whereas some examples are provided in the *Examples* section of the `full documentation web page <https://fredeco.readthedocs.io/en/latest/index.html>`_ of the package. It is strongly recommanded to read that section.

* Each user of ``fredeco`` should have his own FRED® API key. To accomodate a new user of ``fredeco``. One of the functions of the package, ``request_api_key()`` allows the user to open the webpage to request a FRED® API key.

* To retrieve data, the user of ``fredeco`` should indicate the ID of an indicator, such as GDP for the US Gross Domestic Product, and GDPCA for the US Real Gross Domestic Product. Data related to an economic indicator, with the function ``fred_series()``, or several indicators, with the function ``fred_multi_series()``, can be retreived. Remember that each user should have her/his own API key as explained previously.

* ``fredeco`` allows its users to retrieve information about an indicator, as illustrated in the section *Examples*. To retrieve information about an indicator, the function ``fred_info_series()`` should be used. 

* Sometimes, a user may not know the ID of an indicator for which she/he whish to retrieve data. The user may indicate one or several keywords in the function ``fred_search()`` to search for indicators.

* ``fredeco`` allows its users to quickly explore key statistics and information related to data retrieved, as follows, where ``df`` is a data frame of one or several indicators retrieved from FRED® API. The ``explore()`` function does not require the user to add a FRED® API key. However, it cannot be used for data frame where the columns names are not FRED® indicators ID. Indeed, in addition to providing some statistics about the indicators, it also retrieves and provides information related to their unit of measurement and their title.

* The package ``fredeco`` has two modules: ``fredData``, where one can find the functions to retrieve and explore FRED® indicators; ``fredSearch``, where once can search for information related to data provided by FRED® API. The search index, in the documentation, can be used to see the description of each function.


=========================
License and terms of use
=========================

* ``fredeco`` is created by Raulin L. Cadet. It is licensed under the terms of the MIT license.
* By using the package ``fredeco``, you are also agreeing to be bound by the FRED® API Terms of Use. The link to these Terms of Use is: `Here <https://fred.stlouisfed.org/docs/api/terms_of_use.html>`_. 
