from distutils.core import setup
from setuptools import find_packages

setup(
    name='cval-lib',
    version='0.0.2.15',
    description='python computer vision active learning library',
    author='DGQ | Cyrill Belyakov',
    author_email='',
    url='https://cval.ai',
    package_dir={
        '': '.',
    },
    packages=find_packages(include=['cval_lib', 'cval_lib.*']),
    install_requires=[
        'pydantic',
        'requests'
    ]
)
