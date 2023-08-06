#!/usr/bin/env python3
import os, sys, platform
from setuptools import setup # type: ignore
from setuptools import Extension

if sys.version_info[0] != 3:
	raise RuntimeError("Python 3.x required")

try:
	from Cython.Build import cythonize # type: ignore
	have_cython = True
except ImportError:
	have_cython = False

ext_modules = None
if have_cython:
	EXTRA_LINK_ARGS = []
	if platform.system() == 'Linux':
	    EXTRA_LINK_ARGS += ['-Wl,--strip-all']
	ext_modules = cythonize([Extension(
		"fsPacker._fspacker",
		sources=["fsPacker/_fspacker.cpp"],
		language='c++',
		extra_compile_args=[
			'-std=c++17',
			'-fPIC',
			'-Os',
			'-Wall',
			'-Wextra',
			'-Wconversion',
			'-fno-strict-aliasing',
			'-fno-rtti',
		],
		extra_link_args=EXTRA_LINK_ARGS,
	)])

pwd = os.path.abspath(os.path.dirname(__file__))

setup(
	name                          = "python-fspacker",
	version                       = "0.3.2",
	description                   = "Fusion Solutions message packer",
	keywords                      = "message pack packer utility fusion solutions fusionsolutions",
	author                        = "Andor `iFA` Rajci - Fusions Solutions KFT",
	author_email                  = "ifa@fusionsolutions.io",
	url                           = "https://github.com/FusionSolutions/python-fspacker",
	license                       = "GPL-3",
	ext_modules                   = ext_modules,
	packages                      = ["fsPacker"],
	long_description              = open(os.path.join(pwd, "README.md")).read(),
	long_description_content_type = "text/markdown",
	zip_safe                      = False,
	python_requires               = ">=3.8.0",
	install_requires              = ["Cython"],
	test_suite                    = "fsPacker.test",
	package_data                  = { "":["py.typed"] },
	classifiers                   = [ # https://pypi.org/pypi?%3Aaction=list_classifiers
		"Development Status :: 4 - Beta",
		"Topic :: Utilities",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
	],
)
