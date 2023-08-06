#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2016-2019 Cyril Desjouy <cyril.desjouy@univ-lemans.fr>
#
# This file is part of libfds
#
# libfds is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libfds is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libfds. If not, see <http://www.gnu.org/licenses/>.
#
#
# Creation Date : 2018-04-10 - 17:52:42
"""
-----------
DOCSTRING

@author: Cyril Desjouy
"""

import platform
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    def finalize_options(self):
        """ https://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py """
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


if platform.system() == 'Windows':
#    libraries = ['msvcrt']
    libraries = []
    extra_compile_args = ["-O2"]
    extra_link_args = []
else:
    libraries = ['m']
    extra_compile_args = ["-O2", "-fopenmp"]
#    extra_compile_args = ["-Ofast", "-fopenmp"]
    extra_link_args = ['-fopenmp']

extensions = [
    Extension(
        'libfds.fields',
        ["libfds/fields.c"],
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Extension(
        'libfds.libdiff',
        ["libfds/libdiff.c"],
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Extension(
        'libfds.libfilt',
        ["libfds/libfilt.c"],
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),

    Extension(
        'libfds.fluxes',
        ["libfds/fluxes.c"],
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Extension(
        'libfds.filters',
        ["libfds/filters.c"],
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Extension(
        'libfds.cutils',
        ["libfds/cutils.c"],
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Extension(
        'libfds.cmaths',
        ["libfds/cmaths.c"],
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),

]


setup(

    name='libfds',
    description="Finite difference library used by nsfds2/3",
    #    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    version='0.1.0',
    license="GPL",
    author="Cyril Desjouy",
    author_email="cyril.desjouy@univ-lemans.fr",
    install_requires=["numpy"],
    cmdclass={'build_ext': build_ext},
    setup_requires=['numpy'],
    ext_modules=extensions,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ]
)
