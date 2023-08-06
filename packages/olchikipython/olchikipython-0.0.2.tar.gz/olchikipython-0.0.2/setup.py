

import os
from setuptools import setup, find_packages

files = ["samples/*/*", "languages/*/*.yaml"]

setup(
    name='olchikipython',
    version='0.0.2',

    install_requires=[
        "ply",
        "PyYAML",
        "Unidecode",
    ],

    # packages=['olchikipython', 'modes', 'filters', 'languages'],
    packages=find_packages(),
    package_data = {'olchikipython' : files },

    entry_points={
        'console_scripts': [
            'olchikipython=olchikipython.olchiki_python:main',
            'ᱚᱞᱪᱦᱤᱠᱤ=olchikipython.olchiki_python:main',
            'ᱚᱞᱪᱦᱤᱠᱤᱯᱭ=olchikipython.olchiki_python:main'
        ]
    }
)
