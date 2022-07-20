#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['click>=7.0', 'pandas', 'fasttext~=0.9.2', 'spacy', 'textdistance']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Software Engineering Laboratory of Fudan University",
    author_email='lmwtclmwtc@outlook.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Provides a knowledge system constructed from functionality categories, verbs, and phrase patterns, as well as functionality for fine-grained analysis of functionality descriptions based on this knowledge system",
    entry_points={
        'console_scripts': [
            'funcverbnet=funcverbnet.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    packages=find_packages(include=['funcverbnet', 'funcverbnet.*']),
    # include_package_data=True,
    package_data={
        # If any package contains *.json files, include them:
        'funcverbnet': [
            "data/*.json",
            "data/*.bin",
            "data/*.zip",
            "data/*.csv",
            "data/*.txt",
            "classifier/model/*.model"
        ],
    },
    keywords='funcverbnet',
    name='funcverbnet',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/FudanSELab/funcverbnet',
    version='0.2.9',
    zip_safe=False,
)
