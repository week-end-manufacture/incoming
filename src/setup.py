#!/usr/bin/env python
import os

from setuptools import setup, find_packages

def get_version():
    version = {}
    version_file_path = os.path.join('libj', 'verlib.py')
    with open(version_file_path) as fp:
        exec(fp.read(), version)
    return version['__version__']


setup(
    name='incoming',
    author='WEEK END MANUFACTURE',
    version=get_version(),
    license='MIT License',
    url='https://github.com/week-end-manufacture/incoming',
    description='Our best file encoder',
    packages=find_packages(include=['libj', 'libj.*']),
    py_modules=['main'],
    install_requires = [
        'setuptools==69.5.1',
        'altgraph==0.17.4',
        'Brotli==1.1.0',
        'colorlog==6.8.2',
        'inflate64==1.0.0',
        'macholib==1.16.3',
        'multivolumefile==0.2.3',
        'packaging==24.0',
        'pillow==10.3.0',
        'psutil==5.9.8',
        'py7zr==0.21.0',
        'pybcj==1.0.2',
        'pycryptodomex==3.20.0',
        'pyinstaller==6.6.0',
        'pyinstaller-hooks-contrib==2024.6',
        'pyppmd==1.1.0',
        'pyzstd==0.15.10',
        'rarfile==4.2',
        'texttable==1.7.0',
        'unrar==0.4',
    ],
    entry_points={
        'console_scripts': [
            'incoming = main:main',
        ]
    },
    python_requires='>=3.6',
)