from setuptools import setup

setup(
    name = 'comathon',
    version = '0.0.1',
    description = 'test',
    py_modules = ["myfunctions"],
    packages = setuptools.find_packages(),
    package_dir = {'': 'comathon'}    
    )