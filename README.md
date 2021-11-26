# PyUBA: Python User Behavior Analysis
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it?
`pyuba` is growth hacking tools library.

## Installation
`pyuba` is on PyPI, so you can use pip to install it:
```bash
$ pip install pyuba
```
## Usage Examples

```python
import pyuba as uba

uba = PyUba()
events = uba.load_dataset(1000)

```
## Requirements
+ numpy==1.21.4
+ pandas==1.3.4
+ matplotlib==3.5.0
+ seaborn==0.11.2
+ plotly==5.4.0
+ scipy==1.7.3


## License
`pyuba` is [Apache-2.0 Licensed](./LICENSE).
