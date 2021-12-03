# PyUBA: Python User Behavior Analysis
[![PyPI version](https://badge.fury.io/py/pyuba.svg)](https://pypi.org/project/pyuba/)
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
from plotly.offline import iplot
import pyuba as uba


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
+ numpy==1.21.4
+ pandas==1.3.4
+ matplotlib==3.5.0
+ seaborn==0.11.2
+ plotly==5.4.0
+ scipy==1.7.3


## License
`pyuba` is [Apache-2.0 Licensed](./LICENSE).
