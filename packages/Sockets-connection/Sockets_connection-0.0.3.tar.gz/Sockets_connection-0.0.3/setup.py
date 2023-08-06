from setuptools import setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup (
    name="Sockets_connection",
    version='0.0.3',
    author="Sridhar",
    url="https://git.selfmade.ninja/SRIDHARDSCV/sockets-python",
    author_email="sridhardscv@gmail.com",
    description="Connect the Multiple devices using Python Sockets with simple ways",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "sockets"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ]
)

