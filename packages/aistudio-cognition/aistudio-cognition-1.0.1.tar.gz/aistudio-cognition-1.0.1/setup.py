# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aistudio_cognition',
 'aistudio_cognition.cognibot',
 'aistudio_cognition.models',
 'aistudio_cognition.nlu',
 'aistudio_cognition.nlu.luis',
 'aistudio_cognition.nlu.luis.models']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json==0.5.6', 'requests==2.31.0']

setup_kwargs = {
    'name': 'aistudio-cognition',
    'version': '1.0.1',
    'description': 'NLU and KM prediction utility for AIStudio',
    'long_description': 'None',
    'author': 'Ankita Nair',
    'author_email': 'ankita.nair@automationedge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
