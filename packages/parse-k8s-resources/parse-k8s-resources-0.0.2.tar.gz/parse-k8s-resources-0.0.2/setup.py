#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2023/7/13 15:30 
@Author : harvey
@File : setup.py.py 
@Software: PyCharm
@Desc: 
@Module
"""

from setuptools import setup, find_packages

import parse_k8s_resources


# Do not edit these constants. They will be updated automatically
# by scripts/update-client.sh.
# CLIENT_VERSION = "22.1.0.11.a3"
CLIENT_VERSION = parse_k8s_resources.__version__
PACKAGE_NAME = "parse-k8s-resources"
# DEVELOPMENT_STATUS = "4 - Beta"
DEVELOPMENT_STATUS = "5 - Production/Stable"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

EXTRAS = {
    # 'adal': ['adal>=1.0.2']
}
REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        if ';' in line:
            requirement, _, specifier = line.partition(';')
            for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
            for_specifier.append(requirement)
        else:
            REQUIRES.append(line)

with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# with open('test-requirements.txt') as f:
#     TESTS_REQUIRES = f.readlines()

setup(
    name=PACKAGE_NAME,
    version=CLIENT_VERSION,
    description="parse k8s resource",
    author_email="harveyzhwei@gmail.com",
    author="harvey",
    license="MIT",
    url="",
    project_urls={

    },
    keywords=["kubectl", "Kubernetes"],
    install_requires=REQUIRES,
    extras_require=EXTRAS,
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    long_description="k8s resources statistics" + "\n" + LONG_DESCRIPTION,
    # long_description_content_type='text/x-rst',
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['parse-k8s-resources=parse_k8s_resources.main:main'],
    },
    # data_files=[('j2_templates',['j2_templates',])],
    classifiers=[
        "Development Status :: %s" % DEVELOPMENT_STATUS,
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)