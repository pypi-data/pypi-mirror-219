#! /usr/bin/env python3
# coding: utf-8

"""
REMINDER:
1- build
./setup.py sdist bdist_wheel
2- basic verifications
twine check dist/*
2.5- Deploy on testpypi (optionnal, site here : https://test.pypi.org/):
twine upload --repository testpypi dist/*
3- upload to PyPi
twine upload dist/*
"""

from django_silly_stripe import __version__
import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="django-silly-stripe",
    version=f"{__version__}",
    description=(
        "Wrapper package for python stripe with Django and/or DRF"
        ),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/byoso/django_silly_stripe",
    author="Vincent Fabre",
    author_email="peigne.plume@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    packages=[
        "django_silly_stripe",
        ],
    # include_package_data=True,
    package_data={'': ['*.txt', '*.html', '*.po', '*.mo', '*.pot']},
    python_requires='>=3.7',
    install_requires=[
        "stripe>=5.4.0",
    ],
    keywords='django stripe',
    # entry_points={
    #     "console_scripts": [
    #         "django_silly_auth=main.cmd:cmd",
    #     ]
    # },
    setup_requires=['wheel'],
)
