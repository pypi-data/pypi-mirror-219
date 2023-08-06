import os
from setuptools import setup, find_packages

# Get the absolute path to the requirements.txt file
requirements_path = r"C:\Users\Tobias\Desktop\Webscrape_Course\Webscrape Course\requirements.txt"
with open(requirements_path) as f:
    requirements = f.read().splitlines()

version = '0.1.15'

setup(
    name='torscrape',
    version=version,
    author='Tore.ofc, rxality',
    author_email='tore.ofc.99@gmail.com',
    description='A webscrape package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/toreofc/TorScrape/',
    project_urls={
        'Bug Tracker': 'https://github.com/toreofc/TorScrape/issues'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': '.'},
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=requirements,
)
