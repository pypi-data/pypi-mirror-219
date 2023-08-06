from setuptools import setup, find_packages
import os

VERSION = os.getenv('PACKAGE_VERSION', None)
print(f"{VERSION=}")

if VERSION is None:
  raise RuntimeError('`PACKAGE_VERSION` not defined.')

setup(
    name='typed-api-framework',
    version=VERSION,
    description='A lightweigt package for concisely defining an api.',
    author='Rui Filipe de Sousa Campos @ Digital Defiance',
    author_email='mail@ruicampos.org',
    url='https://github.com/Digital-Defiance/typed-api',
    packages=find_packages(),
    long_description="A lightweigt package for concisely defining an api.",
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'starlette==0.30.0',
        'pydantic==1.10.8',
        'uvicorn==0.22.0',
    ],
)