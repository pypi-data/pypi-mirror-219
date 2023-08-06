from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scatterplot", 
    version="0.1.0",
    author="Sameh Salah",
    author_email="samehsalah83@gmail.com",
    description="A customizable scatter plot package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samehsalah",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "matplotlib>=3.0.0",
        "numpy", 
    ],
)