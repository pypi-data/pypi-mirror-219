import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oceanograpy",
    version="0.0.8",
    author="Andy Banks",
    author_email="",
    description="Toolbox for importing and plotting ADCP and CTD data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" ",
    packages=["oceanograpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)