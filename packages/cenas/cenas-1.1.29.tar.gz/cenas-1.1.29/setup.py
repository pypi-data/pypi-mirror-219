from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        os.system('python post_install.py')

setup(
    name='cenas',
    version='1.1.29',
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