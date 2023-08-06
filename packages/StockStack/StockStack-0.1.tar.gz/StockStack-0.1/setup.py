from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='StockStack',
    version='0.1',
    author='Carlo Bortolan',
    author_email='carlobortolan@gmail.com',
    description='Look up and plot current stock prices from your terminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/carlobortolan/StockStack',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'stockstack=stockstack.caller:main'
        ]
    },
    install_requires=[
        'yfinance',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
