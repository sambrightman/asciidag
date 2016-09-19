# noqa: D100
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from __future__ import division, print_function
import re

from setuptools import setup, find_packages


def main():  # noqa: D103
    with open("asciidag/__init__.py") as init:
        metadata = dict(re.findall(r"__([a-z]+)__\s*=\s*['\"]([^'\"]*)['\"]",
                                   init.read()))

    if not metadata:
        raise RuntimeError("Cannot find metadata information")

    with open("README.rst") as readme:
        readme = readme.read()

    setup(
        name=metadata["title"],
        version=metadata["version"],
        description="Draw DAGs (directed acyclic graphs) as ASCII art, à la git log --graph",  # noqa: E501
        long_description=readme,
        author=metadata["author"],
        author_email=metadata["email"],
        url=metadata["url"],
        packages=find_packages(),
        package_data={metadata["title"]: ["LICENSE"]},
        include_package_data=True,
        setup_requires=[
            'pytest-runner',
        ],
        install_requires=[
            'enum34',
        ],
        tests_require=[
            "flake8_docstrings",
            "flake8",
            "pylint-venv",
            "pylint",
            "pytest-cov",
            "pytest-flake8",
            "pytest-pylint",
            "py>=1.4.29",
            "pytest>=2.7",
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


if __name__ == "__main__":
    main()
