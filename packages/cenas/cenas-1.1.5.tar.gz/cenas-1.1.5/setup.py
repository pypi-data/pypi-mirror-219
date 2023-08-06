from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.call(['cenas-post-install'])

setup(
    name='cenas',
    version='1.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        # Add any other dependencies here
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'cenas=cenas.views:run',
            'cenas-post-install=cenas.scripts.post_install:run_post_install',
        ],
    },
)
