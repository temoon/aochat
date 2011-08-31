#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Setup for AO Chat.
"""


from distutils.core import setup


setup(
    name         = "aochat",
    version      = "0.1.1.8a",
    description  = "Python implementation of Anarchy Online chat protocol.",
    author       = "Tema Novikov",
    author_email = "temoon@temoon.pp.ru",
    download_url = "https://github.com/temoon/aochat",
    
    packages = (
        "aochat",
        "aochat.core"
    ),
    
    package_dir = {
        "aochat": "lib/aochat",
        "aochat.core": "lib/aochat/core",
    },
    
    scripts = (
        "bin/aochat",
    ),
    
    data_files = (
        ("/usr/local/etc", ("etc/aochat.conf",)),
        ("/var/lib/aochat", ("data/texts.dat",)),
    ),
    
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
