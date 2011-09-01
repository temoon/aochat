#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Setup for AO Chat.
"""


from distutils.core import setup


setup(
    name         = "aochat",
    version      = "0.2.0.10a",
    description  = "Python implementation of Anarchy Online chat protocol.",
    author       = "Tema Novikov",
    author_email = "temoon@temoon.pp.ru",
    download_url = "https://github.com/temoon/aochat",
    
    packages = (
        "aochat",
    ),
    
    package_dir = {
        "aochat": "lib/aochat",
    },
    
    classifiers = (
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
