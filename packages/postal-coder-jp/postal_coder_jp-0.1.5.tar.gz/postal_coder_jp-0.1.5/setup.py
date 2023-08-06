# -*- coding:utf-8 -*-
from setuptools import setup


with open("README.rst", encoding="utf-8") as f:
    readme = f.read()


setup(
    name='postal_coder_jp',
    version='0.1.5',
    url='https://pickerlab.net',
    long_description=readme,
    author='picker.',
    author_email='hikaru.tokuhara@chionanthus.jp',
    description='postal_coder_jp is a Python module for geocoding Japanese postal codes.',
    license="MIT",
    install_requires=[],
    packages=['postal_coder_jp'],
    include_package_data=True,
)
