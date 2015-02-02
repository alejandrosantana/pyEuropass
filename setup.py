#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='py2_europass',
    version='0.0.1',
    author=u'Alejandro Santana',
    author_email='tech@alejandrosantana.eu',
    # packages=['requests'],
    packages=find_packages(),
    url='https://github.com/u/alejandrosantana/py2_europass',
    license='GNU AGPLv3 licence, see LICENCE.txt',
    description=('Allows to send json data to Europass interoperability '
                 'platform to receive pdf, doc, odt or xml files containing'
                 'CV, ESP or CV+ESP'),
    long_description=open('README.txt').read(),
    zip_safe=False,
)
