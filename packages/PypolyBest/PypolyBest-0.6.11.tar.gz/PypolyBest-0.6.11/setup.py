# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r") as f:
    long_description =f.read()
setup( name="PypolyBest",
       version="0.6.11",
       description="see long description",
       long_description=long_description,
       long_description_content_type="text/markdown",
       author="Ujjawal",
       url = "",
       author_email="ujjawald21@iitk.ac.in",
       packages=['PypolyBest'],
       install_requires=['scikit-learn'],
       classifiers=[
           "Programming Language :: Python :: 3.8",
           "Operating System :: OS Independent"
           ]
       #extras_require = {
           #"dev": [
            #       "pytest>=3.7",
             #  ]
           #}
       )

