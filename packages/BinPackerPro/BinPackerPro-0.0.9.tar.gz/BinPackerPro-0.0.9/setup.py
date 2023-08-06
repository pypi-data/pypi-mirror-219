from distutils.core import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()
setup(
    name="BinPackerPro",
    packages=["BinPackerPro"],
    version="0.0.9",
    license="MIT",
    description="bin packer pro",
    author="Shaik Arshad",
    author_email="smdar7@example.com",
    # url = 'https://github.com/pypa/binpackerpro',
    install_requires=[
        "matplotlib==3.3",
        "more-itertools",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
    ],
    long_description=readme,
    long_description_content_type="text/markdown",
)
