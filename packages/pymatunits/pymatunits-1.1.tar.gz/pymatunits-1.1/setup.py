from setuptools import setup, find_packages
import pymatunits

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pymatunits',
    version=pymatunits.__version__,
    author='Adam Cox',
    author_email='adam.cox@asdl.gatech.edu',
    description='Package for handling unit systems and materials',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'pint']
)
