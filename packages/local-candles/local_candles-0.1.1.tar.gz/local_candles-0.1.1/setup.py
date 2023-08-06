# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local_candles', 'local_candles.models', 'local_candles.sources']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.2,<3.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'local-candles',
    'version': '0.1.1',
    'description': 'Candles (ohlc) loaders and cache',
    'long_description': '# Local candles\n\n[![PyPI version](https://badge.fury.io/py/local-candles.svg)](https://badge.fury.io/py/local-candles)\n[![Python Versions](https://img.shields.io/pypi/pyversions/local-candles.svg)](https://pypi.python.org/pypi/local-candles/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nUsage example:\n```python\nfrom local_candles import load_candles\n\n\ndef main():\n    df = load_candles(\n        source="binance_futures_ohlc",\n        start_ts="2021-01-01",\n        stop_ts="2021-02-01",\n        interval="1d",\n        symbol="BTCUSDT",\n    )\n\n    print(df)\n\n\nif __name__ == "__main__":\n    main()\n```\n',
    'author': 'Oleksandr Polieno',
    'author_email': 'polyenoom@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nanvel/local-candles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
