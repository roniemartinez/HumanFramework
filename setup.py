#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from setuptools import setup

from human_framework import __version__


setup(
    version=__version__,
    download_url=f'https://github.com/roniemartinez/HumanFramework/tarball/{__version__}'
)
