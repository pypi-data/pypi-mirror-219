from setuptools import setup, find_packages

setup(
    name="dummy_url_wrapper",
    version="0.0.8",
    description="This package provides the wrapping of URLs for not exposing to clients",
    url="https://github.com/nk2909/Python-SDK.git",
    author="Nishant Kabariya",
    author_email="testurl@yopmail.com",
    install_requires=["python-dotenv", "requests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["python"],
    packages=find_packages(),
)
