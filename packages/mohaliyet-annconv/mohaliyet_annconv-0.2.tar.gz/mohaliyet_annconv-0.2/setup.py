# setup.py

from setuptools import setup, find_packages

setup(
    name='mohaliyet_annconv',
    version='0.2',
    description='A utility for converting object detection annotations between different formats.',
    author='Mohammed Aliy',
    author_email='mohammed@mohaliy.et',
    url='https://www.mohaliy.et',
    packages=find_packages(),
    install_requires=['pillow'],
    entry_points={
        'console_scripts': [
            'mohaliyet_annconv = annotation_converter.main:main',
        ],
    },
)
