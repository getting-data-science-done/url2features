# -*- coding: utf-8 -*-
 
"""setup.py: setuptools control."""
 
import re
from setuptools import setup
 
version = re.search(
        '^__version__\s*=\s*"(.*)"',
        open('url2features/__init__.py').read(),
        re.M
    ).group(1)
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
      license="MIT",
      name = "url2features",
      packages = ["url2features"],
      install_requires=[
        'pandas','numpy','sklearn','whois','dnspython','geocoder'
      ],
      include_package_data=True,
      entry_points = {
        "console_scripts": ['url2features = url2features.cli:main']
      },
      version = version,
      description = "Python command line application to extract features from a column of URLs inside a CSV or TSV dataset.",
      long_description = long_descr,
      long_description_content_type='text/markdown',
      author = "John Hawkins",
      author_email = "johnc@getting-data-science-done.com",
      url = "http://getting-data-science-done.com",
      project_urls = {
          'Documentation': "http://url2features.readthedocs.io",
          'Source': 'https://github.com/getting-data-science-done/url2features',
          'Tracker': 'https://github.com/getting-data-science-done/url2features/issues',
      },
    )


