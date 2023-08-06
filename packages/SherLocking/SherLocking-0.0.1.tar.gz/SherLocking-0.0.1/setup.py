from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Applies activation for any program.'
LONG_DESCRIPTION = 'A package to apply activation required to run any program, like a license.'

setup(
    name="SherLocking",
    version=VERSION,
    author="Armando Chaparro",
    author_email="<pylejandria@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[

    ],
    keywords=['python', 'locking', 'activation', 'trial', 'license'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)