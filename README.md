# PyUBA: Python User Behavior Analysis
[![PyPI version](https://badge.fury.io/py/pyuba.svg)](https://badge.fury.io/py/pyuba)
[![GitHub license](https://img.shields.io/github/license/ds-wook/pyuba)](https://github.com/ds-wook/pyuba/blob/main/LICENSE)
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
from plotly.offline import iplot

events = uba.load_dataset(1000)

events = uba.acquisition_events_cohort(
    events=events,
    acquisition_event_name="Install"
)

fig = uba.plot_users_per_period(
    events=events,
    acquisition_event_name="Install",
    user_source_col="user_source",
    period="m",
)

iplot(fig)
```
## Requirements
+ numpy
+ pandas
+ matplotlib
+ seaborn
+ plotly
+ scipy


## License
`pyuba` is [Apache-2.0 Licensed](./LICENSE).
