import os
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        home_dir = os.path.expanduser("~")
        bin_dir = os.path.join(home_dir, ".local", "bin")

        if bin_dir not in os.environ["PATH"]:
            os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"

setup(
    name='cenas',
    version='1.1.30',
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
    },
)
