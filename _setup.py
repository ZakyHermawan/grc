from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import atexit
import os
import sys

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        print("post install script")

setup(
    name='grc',
    version='3.10.0.0',
    description='Example package to print hello world on pip install',
    author='Zaky Hermawan',
    author_email='zaky.hermawan9615@gmail.com',
    license='MIT',
    url='https://github.com/ZakyHermawan/grc',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'hello_world = grc.main:main_function',
        ],
    },
    package_data={
        'grc': ['data/*.dat'],
    },
)
