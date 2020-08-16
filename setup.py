from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sqlpipe',
    version='0.1',
    description='A simple way to run multiple SQL script pipelines in parallel.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mariotaddeucci/sqlpipe',
    keywords='sql pipeline etl parallel redshift postgres postgresql',
    author='Mario Taddeucci',
    author_email='mariotaddeucci@gmx.com',
    license='MIT',
    packages=['sqlpipe'],
    zip_safe=False,
    install_requires=['asyncpg==0.21.0']
)
