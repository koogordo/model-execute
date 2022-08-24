import os

from setuptools import setup, find_packages

PYTHON_VERSION = '3.10'
VERSION = '1.0.0'

setup(
    name='controlplane',
    version=f'{VERSION}',
    author="koogordo",
    author_email="koo.m.gordon@outlook.com",
    description="Model execution for large files",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['boto3', 'redis',
                      'requests', 'psycopg2==2.9.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
