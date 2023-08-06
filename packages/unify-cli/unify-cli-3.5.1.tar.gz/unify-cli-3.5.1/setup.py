# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless requieed by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
from setuptools import setup
from setuptools import find_packages
import re
import subprocess

import semver

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


# Some regexes for parsing semver prerelease tags
GIT_STANDARD_RE = re.compile('^([1-9][0-9]*)-g([0-9a-z]*)$')
GIT_EXTRA_RE = re.compile('^(.*)-([1-9][0-9]*)-g([0-9a-z]*)$')
GIT_DIRTY_RE = re.compile('^([1-9][0-9]*)-g([0-9a-z]*-dirty)$')
def pythonSaneVersion(git_describe):
    """
    Creates a version string that python is happy with.

    Python doesn't care for semver syntax, so we need to create a valid string from an arbitrary semver
    """
    def toPep440(non_num):
        commits = 0
        hashval = None
        # This is probably of the form -NUMBER-SHA_ABBREV so start there
        std_match = GIT_STANDARD_RE.match(non_num)
        if std_match:
            commits = int(std_match.group(1))
            hashval = std_match.group(2)
            return f'dev{commits}+git{hashval}'

        extra_match = GIT_EXTRA_RE.match(non_num)
        if extra_match:
            semver_rel_info = extra_match.group(1)
            commits = int(extra_match.group(2))
            hashval = extra_match.group(3)
            return f'dev{commits}+git{hashval}-{semver_rel_info}'

        dirty_match = GIT_DIRTY_RE.match(non_num)
        if dirty_match:
            commits = int(dirty_match.group(1))
            hashval = dirty_match.group(2)
            return f'dev{commits}+git{hashval}'

        raise Exception(f'Could not parse the prerelease marker from the semver: {non_num}')

    v = semver.Version.parse(git_describe)

    prerelease_clean = None
    if v.prerelease:
        prerelease_clean = toPep440(v.prerelease)

    cleaned = semver.Version(
            major=v.major,
            minor=v.minor,
            patch=v.patch,
            prerelease=prerelease_clean
        )

    return str(cleaned)

version = pythonSaneVersion(os.popen('git describe --dirty').read().strip())

setup(
    name='unify-cli',
    version=str(version),
    description="Element Unify command line tool",
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.csv']},
    hiddenimports=[
        'click',
        'setuptools',
        'unify-sdk',
        'pandas',
    ],
    install_requires=[
        'click',
        'setuptools',
        'unify-sdk',
        'pandas'
    ],
    url='https://github.com/ElementAnalytics/element-unify-cli',
    author='Element Analytics',
    author_email='platform@ean.io',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points='''
        [console_scripts]
        ah=source.ah:cli
        unify=source.ah:cli
    ''',
)
