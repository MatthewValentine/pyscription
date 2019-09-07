import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyscription",
    version="0.0.1",
    author="Matthew Valentine",
    author_email="matthew.aaron.valentine@gmail.com",
    description="Command line scripting utilies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewvalentine/pyscription",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
