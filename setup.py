from setuptools import setup, find_packages

setup(
    name='hydra_python_core',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='Core functions for Hydrus',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/HTTP-APIs/hydra-python-core',
    zip_safe=False
)