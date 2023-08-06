from setuptools import setup

setup(
    name='salure_helpers_azure',
    version='1.2.1',
    description='Azure wrapper from Salure',
    long_description='Azure wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.azure"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'azure-storage-file-share>=12.6.0',
        'azure-storage-blob>=12.16.0',
        'msal==1.22.0'
    ],
    zip_safe=False,
)
