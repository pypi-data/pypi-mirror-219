from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vsss_client",
    version="0.1.3",
    author="Lucas de Felippe & Lucas Martins",
    url="https://github.com/fbot-furg/vsss-client.git",
    install_requires=[
        "configparser",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License'
    ],
    packages=['vsss_client']
)   
