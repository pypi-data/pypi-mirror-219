#!/usr/bin/env python

"""The setup script."""
import time
from pathlib import Path
from setuptools import setup, find_packages

DIR = Path(__file__).resolve().parent
version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="yuanjie",
    author_email='313303303@qq.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Create a Python package.",
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='xx-apollo',
    name='xx-apollo',

    packages=find_packages(include=['apollo', 'apollo.*']),

    test_suite='tests',
    url='',
    version=version,  # '0.0.0',
    zip_safe=False,
)
