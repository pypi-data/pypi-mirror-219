from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='fastpdf',
    version='0.0.2',
    url='https://github.com/fastpdfservices/fastpdf-python',
    author='Korian',
    author_email='korian@fastpdfservice.com',
    description='SDK for PDF rendering, generation & transformation via Fast PDF Service. Visit https://fastpdfservice.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),    
    install_requires=[
     'requests',
     'python-magic'
     ],
     classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
