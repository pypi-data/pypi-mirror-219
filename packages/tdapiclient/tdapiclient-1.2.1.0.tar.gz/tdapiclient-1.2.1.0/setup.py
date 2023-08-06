# ##################################################################
#
# Copyright 2022 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: pt186002@teradata.com
# Secondary Owner:
#
# This file installs tdsagemaker library.
# ##################################################################

import sys
import platform
from setuptools import setup, find_packages
from tdapiclient._version import version

# Making sure correct platform is being used i.e. 64 bit.
if platform.architecture()[0] != '64bit':
    print("Unsupported platform !!")
    sys.exit(1)

with open('tdapiclient/README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='tdapiclient',
      version=version,
      author='Teradata Corporation',
      description='Teradata API Client Python package',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://www.teradata.com/',
      license='Teradata License Agreement',
      keywords='Teradata',
      package_data={'': ['README.md', 'LICENSE.txt', 'LICENSE-3RD-PARTY.pdf']},
      packages=find_packages(exclude=("*.tests",
                                      "*.tests.*", "tests.*", "tests")),
      platforms=['MacOS X, Windows, Linux'],
      python_requires='>=3.0',  # TeradataML requires python3,
                                # so we this option is kept
      install_requires=['teradataml >= 17.20.00.03', 'sagemaker >= 2.75.00',
                        'azure-mgmt-storage >= 19.0.0',
                        'azure-storage-blob >= 12.14.0',
                        'azureml-core >= 1.42.0'],
      zip_safe=True,
      classifiers=(
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Topic :: Database :: Front-Ends',
        'License :: Other/Proprietary License',
      ))
