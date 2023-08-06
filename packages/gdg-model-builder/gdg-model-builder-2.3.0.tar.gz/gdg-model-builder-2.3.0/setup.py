# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdg_model_builder',
 'gdg_model_builder.clock',
 'gdg_model_builder.collection',
 'gdg_model_builder.data',
 'gdg_model_builder.model',
 'gdg_model_builder.schedule',
 'gdg_model_builder.shape',
 'gdg_model_builder.state',
 'gdg_model_builder.util',
 'gdg_model_builder.watcher']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.4.0,<22.0.0',
 'cattrs>=22.1.0,<23.0.0',
 'checksumdir>=1.2.0,<2.0.0',
 'dask>=2023.3.2,<2024.0.0',
 'fastapi[all]>=0.78.0,<0.79.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'numpy>=1.23.0,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pottery>=3.0.0,<4.0.0',
 'pycron>=3.0.0,<4.0.0',
 'redis>=4.3.4,<5.0.0']

setup_kwargs = {
    'name': 'gdg-model-builder',
    'version': '2.3.0',
    'description': '',
    'long_description': None,
    'author': 'Liam Monninger',
    'author_email': 'l.mak.monninger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.9,<4.0',
}


setup(**setup_kwargs)
