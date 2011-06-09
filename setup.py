#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Setup for AO Chat.
"""


from distutils.core import setup


setup(
    name         = "aochat",
    version      = "0.0.2.2pa",
    description  = "Python implementation of Anarchy Online chat protocol.",
    author       = "Tema Novikov",
    author_email = "temoon@temoon.pp.ru",
    download_url = "https://github.com/temoon/aochat",
    
    packages = [
        "AOChat",
    ],
    
    package_dir = {
        "AOChat": "lib/AOChat",
    },
    
    classifiers = (
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
