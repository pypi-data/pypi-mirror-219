# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 11:19:19 2022

@author: manou
"""

from setuptools import setup
import tfe22540


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='alcoholic_tfe22540',
    version='0.1.10',
    description='Framework of my master thesis on the effect of withdrawal on the white matter of alcoholic patients using dMRI data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mdausort/TFE22-540',
    author='Manon Dausort',
    author_email='manon.dausort@uclouvain.be',
    license='BSD 2-clause',
    packages=['tfe22540'],
    install_requires=['numpy',
                      'nibabel',
                      'xlsxwriter',
                      'pandas',
                      'matplotlib',
                      'sklearn',
                      'seaborn',
                      'dipy',
                      'scikit-image',
                      'scipy',
                      'openpyxl'
                      ],

    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
    ],
)
