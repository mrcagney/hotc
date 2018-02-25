from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name='hotc',
    version='0.0.0',
    author='Alex Raichev',
    url='https://github.com/araichev/hotc',
    description='A Python 3.5+ library to get Heart of the City walking counts for Auckland, New Zealand',
    long_description=readme,
    license=license,
    install_requires=[
        'pandas>=0.20',
        'requests-futures>=0.9.7',
    ],
    packages=find_packages(exclude=('tests', 'docs'))
)

