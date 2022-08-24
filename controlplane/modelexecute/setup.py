import os

from setuptools import setup, find_packages

PYTHON_VERSION = '3.10'
VERSION = '1.0.0'

setup(
    name='modelexecute',
    version=f'{VERSION}',
    author="koogordo",
    author_email="koo.m.gordon@outlook.com",
    description="Model execution for large files",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['boto3',
                      'requests', 'psycopg2==2.9.3', 'SQLAlchemy==1.4.40'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
