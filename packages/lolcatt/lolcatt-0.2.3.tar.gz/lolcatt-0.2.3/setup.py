#!/usr/bin/env python
"""The setup script."""
from pkg_resources import parse_requirements
from setuptools import find_packages
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

history = ''

with open('requirements/prod.txt') as prod_req:
    requirements = [str(ir) for ir in parse_requirements(prod_req)]
with open('requirements/test.txt') as test_req:
    test_requirements = [str(ir) for ir in parse_requirements(test_req)]

setup(
    author="Lukas Lüftinger",
    author_email='lukas.lueftinger@outlook.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="A TUI wrapper around `catt`.",
    entry_points={
        'console_scripts': [
            'lolcatt=lolcatt.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lolcatt',
    name='lolcatt',
    packages=find_packages(include=['lolcatt', 'lolcatt.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/LokiLuciferase/lolcatt',
    version='0.2.3',
    zip_safe=False,
)
