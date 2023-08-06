from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        # Add the directory to PATH
        bin_dir = os.path.join(sys.prefix, 'bin')
        if bin_dir not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + bin_dir

setup(
    name='cenas',
    version='1.1.26',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'cenas=cenas.views:run',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    }
)