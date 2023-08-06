#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='timez',
    version='0.0.1',
    author='Avins Wang',
    author_email='avinswang@gmail.com',
    url='https://github.com/AvinsWang/timez',
    download_url="http://pypi.python.org/pypi/timez",
    description="Easy time class supporting chain called, deprecated name: py-itime",
    long_description=open(os.path.join(here, 'ReadMe.rst')).read(),
    license='LGPL-3.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords=['timez', 'py-itime', 'python time'],
    classifiers=['Topic :: Utilities', 
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Programming Language :: Python :: 3.6'],
)
