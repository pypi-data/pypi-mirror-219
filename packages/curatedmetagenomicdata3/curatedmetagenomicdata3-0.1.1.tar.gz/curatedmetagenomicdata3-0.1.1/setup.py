from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='curatedmetagenomicdata3',
    version='0.1.1',
    packages=find_packages(),
    author_email="skhan8@mail.einstein.yu.edu",
    description="Python wrapper for curatedMetagenomicData3.",
    long_description=open('README.md').read(),
    url="https://github.com/kellylab/curatedmetagenomidata3-python",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
