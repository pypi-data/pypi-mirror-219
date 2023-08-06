# Copyright (c) 2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(name='picotalk',
      version='0.0.21',
      description='Simple voice call tool.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='voice call',
      classifiers=[
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3.8'
      ],
      url='https://codeberg.org/tok/picotalk',
      author='T. Kramer',
      author_email='code@tkramer.ch',
      license='AGPL v3',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'picotalk-client = picotalk.client:main',
              'picotalk-server = picotalk.server:main'
          ]
      },
      install_requires=[
          'pyaudio',
          'pynacl',
          'numpy',  # BSD
          'scipy',  # BSD
      ],
      zip_safe=False)
