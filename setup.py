# Copyright (C) 2011 Dan Colish
# All rights reserved.
#
# This file is part of 'Work' and is distributed under the GPLv3 license.
# See LICENSE for more details.

from setuptools import find_packages, setup

description = ''
with open('README.rst') as f:
    description = f.read()

setup(name='Work',
      version='dev',
      description='Agile work time tracker',
      long_description=description,
      packages=find_packages(),
      author='Dan Colish',
      author_email='dcolish@gmail.com',
      license='GPLv3',
      platforms='any',
      entry_points={
        'console_scripts': [
            'work=work.frontend:main',
            ],
        },
      )
