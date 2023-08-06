from setuptools import setup

setup(
    name='lotr_api_rr',
    version='0.1.1',
    author='Roman Rochowniak',
    author_email='roman.rochowniak@gmail.com',
    description='LotR API client',
    license='BSD',
    packages=['lotr_api'],
    long_description='LotR API client',
    install_requires=[
        'requests',
        'pydantic',
    ]
)
