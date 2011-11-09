# Copyright (C) 2011 Dan Colish
# All rights reserved.
#
# This file is part of 'Work' and is distributed under the GPLv3 license.
# See LICENSE for more details.

from setuptools import find_packages, setup


setup(name='Work',
      version='dev',
      packages=find_packages(),
      author='Dan Colish',
      author_email='dcolish@gmail.com',
      license='GPLv3',
      platforms='any',
      entry_points={
        'console_scripts': [
            'timer=timer.frontend:main',
            ],
        },
      )
