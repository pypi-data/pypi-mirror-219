from setuptools import setup, find_packages

setup(
    name='cenas',
    version='1.1.11',
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
