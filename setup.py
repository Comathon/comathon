from setuptools import setup, find_packages

setup(
    name = 'comathon',
    version = '0.0.1',
    license = 'MIT',
    author = 'Comathon',
    author_email='Comathon2020@gmail.com',
    description = 'test',
    py_modules = ["myfunctions"],
    packages = find_packages(),
    package_dir = {'': 'comathon'},
    url='https://github.com/Comathon/module'

    )