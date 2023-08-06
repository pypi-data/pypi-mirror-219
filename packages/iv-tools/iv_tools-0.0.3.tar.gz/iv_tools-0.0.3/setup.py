# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 20:07:59 2023

@author: varun
"""

from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'IV Tools'
LONG_DESCRIPTION = 'Implied Volatility Tools'

# Setting up
setup(
    name="iv_tools",
    version=VERSION,
    author="varun",
    author_email="varunsrikanth91@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)