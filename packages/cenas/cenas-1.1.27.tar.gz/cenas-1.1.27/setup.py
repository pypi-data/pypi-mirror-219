from setuptools import setup, find_packages
import site
import sys

# Get the user site packages directory
site_packages = site.getusersitepackages()

# Add the user site packages directory to the PATH
if site_packages not in sys.path:
    sys.path.append(site_packages)

setup(
    name='cenas',
    version='1.1.27',
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
)
