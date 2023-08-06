from setuptools import setup, find_packages



setup(
    name='afeSMS',
    version='1.0.0',
    description='afe SMS sender Python package',
    author='Morteza Sotoodeh',
    author_email='sotoodeh@afe.ir',
    packages=['afeSMS'],
    install_requires=[
        'requests',
        'zeep',
    ],
)
