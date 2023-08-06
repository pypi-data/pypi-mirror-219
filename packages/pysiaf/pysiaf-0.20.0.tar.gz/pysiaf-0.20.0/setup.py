#!/usr/bin/env python
import os
import pkgutil
import platform
import sys
from setuptools import setup, find_packages, Extension, Command
from setuptools.command.test import test as TestCommand

try:
    from distutils.config import ConfigParser
except ImportError:
    from configparser import ConfigParser

conf = ConfigParser()
conf.read(['setup.cfg'])

# Get some config values
metadata = dict(conf.items('metadata'))
PACKAGENAME = metadata.get('package_name', 'packagename')
DESCRIPTION = metadata.get('description', '')
AUTHOR = metadata.get('author', 'STScI')
AUTHOR_EMAIL = metadata.get('author_email', 'help@stsci.edu')
URL = metadata.get('url', 'https://www.stsci.edu/')
LICENSE = metadata.get('license', 'BSD')


# allows you to build sphinx docs from the pacakge
# main directory with python setup.py build_sphinx

try:
    from sphinx.cmd.build import build_main
    from sphinx.setup_command import BuildDoc

    class BuildSphinx(BuildDoc):
        """Build Sphinx documentation after compiling C source files"""

        description = 'Build Sphinx documentation'

        def initialize_options(self):
            BuildDoc.initialize_options(self)

        def finalize_options(self):
            BuildDoc.finalize_options(self)

        def run(self):
            build_cmd = self.reinitialize_command('build_ext')
            build_cmd.inplace = 1
            self.run_command('build_ext')
            build_main(['-b', 'html', './docs', './docs/_build/html'])

except ImportError:
    class BuildSphinx(Command):
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            # print('!\n! Sphinx is not installed!\n!', file=sys.stderr)
            raise RuntimeError('!\n! Sphinx is not installed!\n!')
            exit(1)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['pysiaf/tests']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

install_requires = [
        'astropy>=4.3.1',
        'lxml>=4.6.4',
        'matplotlib>=3.4.3',
        'numpy>=1.21.4',
        'numpydoc>=1.1.0',
        'openpyxl>=3.0.9',
        'requests>=2.26.0',
        'scipy>=1.7.2',
    ]

# Patch because MacOS Mojave causes matplotlib to fail without pyqt5 - will remove line if this bug is patched
# Also noted as a known installation issue in the project's README
if platform.system().lower() == 'darwin' and platform.mac_ver()[0].split('.')[0:2] == ['10', '14']:
    try:
        import PyQt5
    except ModuleNotFoundError:
        install_requires.append('PyQt5')

setup(
    name=PACKAGENAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    setup_requires=['setuptools_scm'],
    use_scm_version={'write_to': os.path.join(PACKAGENAME, 'version.py')},
    install_requires=install_requires,
    extras_require={
        'docs': ['stsci_rtd_theme',
                 'sphinx_automodapi',
                 'numpy',
                 'matplotlib',
                 'scipy']
    },
    tests_require=['pytest'],
    packages=find_packages(),
    package_data={PACKAGENAME: ['prd_data/HST/*',
                                'prd_data/JWST/*/*/*/*.xlsx',
                                'prd_data/JWST/*/*/*/*.xml',
                                'pre_delivery_data/*/*.*',
                                'source_data/*/*/*.txt',
                                'source_data/*/*.txt',
                                'source_data/*.txt',
                                'tests/test_data/*/*/*/*.fits',
                                'tests/test_data/*/*/*/*.txt',
                                ]},
    cmdclass={
        'test': PyTest,
        'build_sphinx': BuildSphinx
    },)
