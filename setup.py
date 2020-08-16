from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sqlpipe',
    version='0.2',
    description='A simple way to run multiple SQL script pipelines in parallel.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mariotaddeucci/sqlpipe',
    keywords='sql pipeline etl parallel redshift postgres postgresql mysql',
    author='Mario Taddeucci',
    author_email='mariotaddeucci@gmx.com',
    license='MIT',
    packages=['sqlpipe'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "asyncpg>=0.21.0",
        "aiomysql>=0.0.20"
    ]
)
