from setuptools import setup, find_packages

try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements

install_requires = parse_requirements('requirements.txt', session=PipSession())
try:
    dependencies = [str(package.requirement) for package in install_requires]
except:
    dependencies = [str(package.req) for package in install_requires]

setup(
    name='hydra_python_core',
    version='0.3',
    packages=find_packages(),
    license='MIT',
    description='Core functions for Hydrus',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=dependencies,
    url='https://github.com/HTTP-APIs/hydra-python-core',
    zip_safe=False,
    author='Hydra Ecosystem',
    author_email='collective@hydraecosystem.org',
)
