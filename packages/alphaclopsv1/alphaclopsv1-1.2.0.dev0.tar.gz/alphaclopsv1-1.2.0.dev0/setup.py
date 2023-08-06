# Copyright 2018 The alphaclops Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
from setuptools import find_packages, setup

# This reads the __version__ variable from alphaclops/_version.py
__version__ = ''
exec(open('alphaclops/_version.py').read())

name = 'alphaclopsv1'

description = (
    'A framework for creating, editing, and invoking '
    'Noisy Intermediate Scale Quantum (NISQ) circuits.'
)

# README file as long_description.
long_description = io.open('README.rst', encoding='utf-8').read()

# If alphaclops_PRE_RELEASE_VERSION is set then we update the version to this value.
# It is assumed that it ends with one of `.devN`, `.aN`, `.bN`, `.rcN` and hence
# it will be a pre-release version on PyPi. See
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#pre-release-versioning
# for more details.
if 'alphaclops_PRE_RELEASE_VERSION' in os.environ:
    __version__ = os.environ['alphaclops_PRE_RELEASE_VERSION']
    long_description = (
        "**This is a development version of alphaclops-core and may be "
        "unstable.**\n\n**For the latest stable release of alphaclops-core "
        "see**\n`here <https://pypi.org/project/alphaclops-core>`__.\n\n" + long_description
    )

# Read in requirements
requirements = open('requirements.txt').readlines()
requirements = [r.strip() for r in requirements]
contrib_requirements = open('alphaclops/contrib/requirements.txt').readlines()
contrib_requirements = [r.strip() for r in contrib_requirements]


alphaclops_packages = ['alphaclops'] + [
    'alphaclops.' + package for package in find_packages(where='alphaclops', exclude=['google', 'google.*'])
]

# Sanity check
assert __version__, 'Version string cannot be empty'

setup(
    name=name,
    version=__version__,
    url='https://news.agpt.co/',
    author='The alphaclops Developers',
    author_email='alphaclops-dev@open.com',
    python_requires=('>=3.9.0'),
    install_requires=requirements,
    extras_require={'contrib': contrib_requirements},
    license='Apache 2',
    description=description,
    long_description=long_description,
    packages=alphaclops_packages,
    package_data={'alphaclops': ['py.typed'], 'alphaclops.protocols.json_test_data': ['*']},
)
