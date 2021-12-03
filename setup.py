from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyuba",
    version="0.0.8",
    author="Wook Lee",
    author_email="leewook94@gmail.com",
    description="growth hacking tool test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ds-wook/pyuba",
    keywords=["growth-hacking", "visualization", "data-analysis"],
    packages=find_packages(),
    install_requires=["numpy", "pandas", "matplotlib", "seaborn", "plotly", "scipy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
