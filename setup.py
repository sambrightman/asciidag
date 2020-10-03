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
        long_description_content_type="text/x-rst",
        author=metadata["author"],
        author_email=metadata["email"],
        url=metadata["url"],
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        include_package_data=True,
        zip_safe=False,
        setup_requires=[
            "pytest-runner",
        ],
        install_requires=[
            "enum34; python_version<'3.4'",
        ],
        tests_require=[
            "astroid<2; python_version<'2.7' or (python_version>='3' and python_version<'3.4')",
            "flake8; (python_version>='2.7' and python_version<'3') or python_version>='3.4'",
            "flake8<3.8; python_version<'2.7' or (python_version>='3' and python_version<'3.4')",
            "flake8_docstrings",
            "isort<5",
            "more-itertools<6",
            "py>=1.4.29",
            "pydocstyle<4",
            "pylint-venv<2",
            "pylint<2; python_version<'3.5'",
            "pylint>=2; python_version>='3.5'",
            "pyparsing<3",
            "pytest-cov; (python_version>='2.7' and python_version<'3') or python_version>='3.4'",
            "pytest-cov<2.6; python_version<'2.7' or (python_version>='3' and python_version<'3.4')",
            "pytest-flake8; (python_version>='2.7' and python_version<'3') or python_version>='3.4'",
            "pytest-flake8<0.9; python_version<'2.7' or (python_version>='3' and python_version<'3.4')",
            "pytest-pylint<0.10; python_version<'2.7' or (python_version>='3' and python_version<'3.4')",
            "pytest-pylint<0.15; (python_version>='2.7' and python_version<'3') or python_version>='3.4'",
            "pytest<3; python_version<'2.7' or (python_version>='3' and python_version<'3.4')",
            "pytest>=2.7,<4.7; (python_version>='2.7' and python_version<'3') or python_version>='3.4'",
            "typed_ast<1.3; python_version>='3' and python_version<'3.5'",
            "typing<3.7; python_version>='3' and python_version<'3.5'",
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
