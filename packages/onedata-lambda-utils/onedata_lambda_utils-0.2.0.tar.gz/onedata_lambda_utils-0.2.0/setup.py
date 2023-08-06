#!/usr/bin/env python

from setuptools import setup

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="onedata_lambda_utils",
    version="0.2.0",
    python_requires=">=3.7",
    description="Python Library containing utility functions for use in OpenFaaS lambda implementations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rafal Widziszewski",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    packages=["onedata_lambda_utils"],
    package_data={"onedata_lambda_utils": ["py.typed"]},
    include_package_data=True,
    install_requires=["typing-extensions==4.3.0"]
)
