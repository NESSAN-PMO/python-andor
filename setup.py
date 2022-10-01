#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup script for python-andor.
"""
import numpy as np
import os
import platform
from setuptools import setup, Extension

system = platform.system()

lib3 = []
inc3 = [np.get_include()]
libdir3 = []
mac3 = []
data3 = []
src3 = [os.path.join("Andor3", "pyandor3.pyx")]

if platform.system() == "Windows":
    inc3 += [os.path.join('andor3_sdk', 'pkg_win', 'include'), 'Andor3']
    lib3 += ["atcorem"]
    if platform.architecture()[0] == "64bit":
        libdir3 += [os.path.join('andor3_sdk', 'pkg_win', 'x64')]
        data3 += [os.path.join('andor3_sdk', 'pkg_win', 'x64', 'atcore.dll')]
    elif platform.architecture()[0] == "32bit":
        libdir3 += [os.path.join('andor3_sdk', 'pkg_win', 'x86')]
        data3 += [os.path.join('andor3_sdk', 'pkg_win', 'x86', 'atcore.dll')]
compiler_settings3 = {
    'libraries': lib3,
    'include_dirs': inc3,
    'library_dirs': libdir3,
    'define_macros': mac3,
    'export_symbols': None,
    'language': 'c++'
}

ext_modules = [Extension("Andor3.pyandor3", src3, **compiler_settings3)]
setup(name='python-andor',
      version='1.0',
      author='Fockez Zhang',
      author_email='fockez@live.com',
      packages=['Andor2', 'Andor3'],
      package_dir={'Andor2': 'Andor2', 'Andor3': 'Andor3'},
      package_data={
          'Andor2': ['atmcdLXD.pxd'],
          'Andor3': ['atcore.pxd']},
      description='Python binding for Andor SDK',
      license='GNU LGPL',
      setup_requires=[
          'setuptools>=28.3',
          'Cython>=0.24'
      ],
      install_requires=[
          'numpy>=1.11',
          'Cython>=0.24'
      ],
      ext_modules=ext_modules,
      )
