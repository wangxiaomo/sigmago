#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages


metadata = {'name': "sigmago",
            'description': "A books-exchanging web community.",
            'version': "0.1-dev",
            'install_requires': [],
            'packages': find_packages(exclude=["tests"]),
            'package_data': {},
            'test_suite': "tests.suite.suite"}


if __name__ == "__main__":
    setup(**metadata)
