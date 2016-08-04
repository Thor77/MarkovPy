# MarkovPy [![Build Status](https://travis-ci.org/Thor77/MarkovPy.svg?branch=master)](https://travis-ci.org/Thor77/MarkovPy) [![Coverage Status](https://coveralls.io/repos/github/Thor77/MarkovPy/badge.svg?branch=master)](https://coveralls.io/github/Thor77/MarkovPy?branch=master) [![Documentation Status](https://readthedocs.org/projects/markovpy/badge/?version=latest)](http://markovpy.readthedocs.io/en/latest/?badge=latest)
A simple Markovchain-Implementation written in Python

# Installation
* `pip3 install markovpy`
* Clone this repo `git clone https://github.com/Thor77/MarkovPy` and run `python3 setup.py install`

# Usage
Initialize a new `MarkovPy`-Instance with an initialized store:
```
from markov.stores import Store
m = markov.MarkovPy(store=Store())
```

## Available stores
#### Pickle
`markov.stores.Pickle`

Using an in-memory-`dict` and `pickle` to persist it between sessions.

#### Redis (requires `redis`)
`markov.stores.Redis`

Using a redis-database.
