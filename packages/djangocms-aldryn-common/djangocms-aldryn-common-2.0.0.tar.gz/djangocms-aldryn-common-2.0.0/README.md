![Continuation of the deprecated project "Divio Aldryn common"](https://img.shields.io/badge/Continuation-Divio_Aldryn_Common-blue)
![Pypi package](https://img.shields.io/pypi/v/djangocms-aldryn-common.svg?link=https%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjangocms-aldryn-common)
![Status](https://img.shields.io/pypi/status/djangocms-aldryn-common.svg?link=https%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjangocms-aldryn-common)
![Python versions](https://img.shields.io/pypi/pyversions/djangocms-aldryn-common.svg?link=https%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjangocms-aldryn-common)
![License](https://img.shields.io/pypi/l/djangocms-aldryn-common.svg?link=https%3A%2F%2Fpypi.python.org%2Fpypi%2Fdjangocms-aldryn-common)

# Aldryn Common

Continuation of the deprecated project [Divio Aldryn Common](https://github.com/divio/aldryn-common).

Aldryn Common is a library of helpful utilities for packages in the [Aldryn](http://aldryn.com) ecosystem, and is
also aimed at developers of [django CMS](http://django-cms.org) projects.

It's installed by default in your Aldryn project - you don't need to do anything to install it - and numerous other
Addons will make use of the tools it provides. Feel free to make use of them in your own projects.

They include tools for:

* pagination
* handling slugs (cleaning, ensuring uniqueness)
* managing times and dates

as well as a variety of helpful templatetags and more.

## Settings:

* ``ALDRYN_COMMON_PAGINATION_SOFTLIMIT``: Soft-limiting search results. If True, querying a page number larger than max.
 will not fail, but instead return the last available page. Default is True.
