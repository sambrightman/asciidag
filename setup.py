# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function
import re

from setuptools import setup

with open("asciidag/__init__.py") as f:
    metadata = dict(re.findall("__([a-z]+)__\s*=\s*['\"]([^'\"]*)['\"]", f.read()))

if not metadata:
    raise RuntimeError("Cannot find metadata information")

with open("README.rst") as f:
    readme = f.read()

setup(
    name=metadata["title"],
    version=metadata["version"],
    description="Draw DAGs (directed acyclic graphs) as ASCII art, à la git log --graph",
    long_description=readme,
    author=metadata["author"],
    author_email=metadata["email"],
    url=metadata["url"],
    # FIXME: find_packages
    packages=[
        metadata["title"],
    ],
    package_data={metadata["title"]: ["LICENSE"]},
    include_package_data=True,
    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
        'enum34',
    ],
    tests_require=[
        "pytest-cov",
        "pytest",
    ],
    license=metadata["license"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development",
    ],
)
