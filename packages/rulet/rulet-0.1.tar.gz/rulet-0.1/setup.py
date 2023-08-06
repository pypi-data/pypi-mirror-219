from setuptools import setup, find_packages

setup(
    name='rulet',
    version='0.1',
    description='Russian Roulette game',
    url='https://github.com/WinterCitizen/roulette',
    entry_points={
        'console_scripts': [
            'rulet = cli.run:main',
        ],
    },
    packages=find_packages(),
)
