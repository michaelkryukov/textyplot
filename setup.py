from setuptools import setup, find_packages
from os.path import join, dirname

import textyplot


setup(
    name='Textyplot',
    version=textyplot.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    test_suite='tests',
    author='Krukov Michael',
    author_email='krukov.michael@ya.ru',
    url='https://github.com/michaelkrukov/textyplot',
    keywords=['diagram', 'graph', 'plotting', 'text'],
    py_modules=['textyplot'],
    entry_points={
        'console_scripts': ['textyplot = textyplot.textyplot:main']
    }
)
