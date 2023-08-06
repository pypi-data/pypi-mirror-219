# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras_eo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'keras-eo',
    'version': '2023.7.14',
    'description': 'Deep Learning for Earth Observation with Keras',
    'long_description': '# kerasEO\nDeep learning for Earth Observation with Keras\n',
    'author': 'Juan Sensio',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
