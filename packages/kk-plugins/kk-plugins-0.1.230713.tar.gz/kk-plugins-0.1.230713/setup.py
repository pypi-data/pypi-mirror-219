#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from pkgutil import walk_packages
from setuptools import setup


def find_packages(path):
    # This method returns packages and subpackages as well.
    return [name for _, name, is_pkg in walk_packages([path]) if is_pkg]


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='kk-plugins',
    version=read_file('VERSION'),
    description="kk plugins",
    long_description=read_file('README.md') + '\n\n' + read_file('HISTORY.md'),
    url='https://github.com/kk-plugins',
    packages=list(find_packages('src')),
    package_dir={'': 'src'},
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
    license="MIT",
    keywords='kk-plugins',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
