# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_astrolab', 'py_astrolab.charts']

package_data = \
{'': ['*'], 'py_astrolab.charts': ['templates/*']}

install_requires = \
['jsonpickle==1.4.2',
 'pdoc',
 'pydantic',
 'pyswisseph==2.8.0.post1',
 'pytest',
 'pytz>=2022.7',
 'requests-cache==0.9.3',
 'requests==2.31.0',
 'terminaltables']

setup_kwargs = {
    'name': 'py-astrolab',
    'version': '0.2.0',
    'description': 'A Python interface on Swiss Ephemeris to perform astrological calculations',
    'long_description': '# Py-Astrolab\n\nA Python interface on Swiss Ephemeris to perform astrological calculations',
    'author': 'Giacomo Battaglia',
    'author_email': 'battaglia.giacomo@yahoo.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
