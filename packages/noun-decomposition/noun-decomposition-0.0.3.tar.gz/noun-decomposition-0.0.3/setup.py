#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noun-decomposition",
    version="0.0.3",
    author="Mathias Haugestad",
    author_email="mhaugestad@gmail.com",
    description="Python module to decompose nouns based on the SECOS algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhaugestad/noun-decomposition",
    packages=setuptools.find_packages(include=['Secos', 'Secos.*']),
    install_requires=['scipy', 'numpy', 'pytest', 'importlib-resources', 'requests', 'tqdm'],
    python_requires='>=3.6',
    download_url='https://github.com/mhaugestad/noun-decomposition/archive/refs/tags/0.0.3.tar.gz'
)