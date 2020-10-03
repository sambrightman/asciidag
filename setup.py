# -*- coding: utf-8 -*-
"""Configuration and metadata for setuptools packaging."""

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function
import re

from setuptools import setup, find_packages


def main():
    """Entrypoint for setuptools."""
    with open("src/asciidag/__init__.py") as init:
        metadata = dict(re.findall(r"__([a-z]+)__\s*=\s*['\"]([^'\"]*)['\"]",
                                   init.read()))

    if not metadata:
        raise RuntimeError("Cannot find metadata information")

    with open("README.rst") as readme:
        readme = readme.read()

    setup(
        name=metadata["title"],
        version=metadata["version"],
        description="Draw DAGs (directed acyclic graphs) as ASCII art, à la git log --graph",
        long_description=readme,
        author=metadata["author"],
        author_email=metadata["email"],
        url=metadata["url"],
        packages=find_packages(where='src'),
        package_dir={'': 'src'},
        include_package_data=True,
        zip_safe=False,
        setup_requires=[
            'pytest-runner',
        ],
        install_requires=[
            'enum34',
        ],
        tests_require=[
            "flake8_docstrings",
            "flake8",
            "isort<5",
            "more-itertools<6",
            "pydocstyle<4",
            "pylint-venv<2",
            "pylint<2;python_version<'3'",
            "pylint>=2;python_version>='3'",
            "pyparsing<3",
            "pytest-cov",
            "pytest-flake8",
            "pytest-pylint<0.15",
            "py>=1.4.29",
            "pytest<4.7,>=2.7",
            "zipp<3",
        ],
        license=metadata["license"],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.0",
            "Programming Language :: Python :: 3.1",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development",
        ],
    )


if __name__ == "__main__":
    main()
