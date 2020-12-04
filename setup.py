#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="seotool",
    version="1.0",
    packages=find_packages(),
    scripts=["crawl.py"],
    install_requires=[
        "beautifulsoup4",
        "Click",
        "pdfkit",
        "requests",
        "urllib3",
        "Markdown",
        "pre-commit",
    ],
)
