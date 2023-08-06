#!/usr/bin/env python3

from setuptools import setup

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name="vmc_reporter",
    description="This package is supposed to prove a Dependency Confusion Attack",
    long_description="This package is supposed to prove a Dependency Confusion Attack",
    version="1.99.100",
    author="Appsec@SBB",
    author_email="application-security@sbb.ch",
    url="https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610",
    packages=["vmc_reporter"],
    python_requires=">=3.10",
    install_requires=["packaging"],
    license="",
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="",
)
