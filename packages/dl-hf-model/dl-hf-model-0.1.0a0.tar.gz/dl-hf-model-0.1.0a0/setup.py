# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dl_hf_model']

package_data = \
{'': ['*']}

install_requires = \
['huggingface-hub>=0.16.4,<0.17.0',
 'install>=1.3.5,<2.0.0',
 'loguru>=0.7.0,<0.8.0',
 'set-loglevel>=0.1.2,<0.2.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['dl-hf-model = dl_hf_model.__main__:app']}

setup_kwargs = {
    'name': 'dl-hf-model',
    'version': '0.1.0a0',
    'description': 'Download and cache a hf model for a given url, save to models dir',
    'long_description': '# dl-hf-model\n[![pytest](https://github.com/ffreemt/dl-hf-model/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/dl-hf-model/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/dl_hf_model.svg)](https://badge.fury.io/py/dl_hf_model)\n\nDownload and cache a huggingface model given a url, save to models dir\n\n## Install it\n\n```shell\npip install dl-hf-model\n# pip install git+https://github.com/ffreemt/dl-hf-model\n# poetry add git+https://github.com/ffreemt/dl-hf-model\n# git clone https://github.com/ffreemt/dl-hf-model && cd dl-hf-model\n```\n\n## Use it\n```python\nfrom dl_hf_model import dl_hf_model\n\n```\n',
    'author': 'ffreemt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffreemt/dl-hf-model',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
