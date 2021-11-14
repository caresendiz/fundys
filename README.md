Fundys

Fundys is a Python library for stock & portfolio analysis.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install fundys
```

## Usage

```python
from fundys import data
from fundys import ratios
from fundys import analysis

# returns the current price
data.price('AAPL')

# returns current ratio annual or quarterly history
ratios.currentRatio('AAPL', 'Y')

# returns portfolio volatility
analysis.portVol(stockHistories, stockWeights)
```.

## License
[MIT](https://choosealicense.com/licenses/mit/)
