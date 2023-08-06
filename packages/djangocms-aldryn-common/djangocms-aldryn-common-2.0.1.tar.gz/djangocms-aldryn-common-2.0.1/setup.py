# -*- coding: utf-8 -*-
from aldryn_common import __version__
from setuptools import find_packages, setup

REQUIREMENTS = [
    'django>=3.2',
    'django-sortedm2m',
]

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 3.2',
    'Framework :: Django :: 4.0',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

setup(
    name='djangocms-aldryn-common',
    version=__version__,
    description='Common utilities',
    long_description=open('README.md').read(),
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/CZ-NIC/djangocms-aldryn-common',
    packages=find_packages(exclude=['tests']),
    license='BSD License',
    platforms=['OS Independent'],
    python_requires='>=3.7',
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
)
