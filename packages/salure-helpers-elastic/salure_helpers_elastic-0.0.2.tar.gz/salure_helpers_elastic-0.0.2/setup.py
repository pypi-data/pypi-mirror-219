from setuptools import setup


setup(
    name='salure_helpers_elastic',
    version='0.0.2',
    description='elastic wrapper from Salure',
    long_description='elastic wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.elastic"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'requests>=2,<=3',
        'paramiko>=2,<=3'
    ],
    zip_safe=False,
)
