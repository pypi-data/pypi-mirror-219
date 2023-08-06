# -*- coding: utf-8 -*-
"""Installer for the collective.restapi.facetedsearch package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='collective.restapi.facetedsearch',
    version='1.0.2',
    description="An add-on for Plone and plone.restapi providing a extended search service",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='muellers',
    author_email='muellers@saw-leipzig.de',
    url='https://git.saw-leipzig.de/muellers/collective.restapi.facetedsearch',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/collective.restapi.facetedsearch',
        'Source': 'https://git.saw-leipzig.de/muellers/collective.restapi.facetedsearch.git',
        'Tracker': 'https://git.saw-leipzig.de/muellers/collective.restapi.facetedsearch/-/issues',
        # 'Documentation': 'https://collective.restapi.facetedsearch.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.restapi'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'plone.api>=1.8.4',
        'plone.restapi',
        'plone.app.dexterity',
        'collective.collectionfilter',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = collective.restapi.facetedsearch.locales.update:update_locale
    """,
)
