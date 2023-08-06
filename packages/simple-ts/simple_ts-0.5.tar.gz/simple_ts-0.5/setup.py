from setuptools import setup

setup(
    name='simple_ts',
    version='0.5',
    description='A simple time series analysis package',
    author='Alisson Louly',
    packages=['simplets'],
    install_requires=['statsmodels', 'matplotlib','pmdarima']
)