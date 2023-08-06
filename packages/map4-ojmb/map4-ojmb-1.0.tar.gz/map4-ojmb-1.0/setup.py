# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='map4-ojmb',
            version='1.0',
            description='MinHashed AtomPair Fingerprint of Radius 2',
            author='Alice Capecchi',
            author_email='alice.capecchi@outlook.it',
            url='https://github.com/OlivierBeq/map4',
            maintainer='Olivier J. M. Béquignon',
            maintainer_email ='olivier.bequignon.maintainer@gmail.com',
            packages=['map4'],
            install_requires=['faerun', 'mhfp', 'rdkit']
           )
