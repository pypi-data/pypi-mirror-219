# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['e2b_agent', 'e2b_agent.routers']

package_data = \
{'': ['*']}

install_requires = \
['fastapi-code-generator>=0.4.2,<0.5.0',
 'fastapi>=0.100.0,<0.101.0',
 'uvicorn[standard]>=0.22.0,<0.23.0']

entry_points = \
{'console_scripts': ['src = src.__main__:main']}

setup_kwargs = {
    'name': 'kuba-test-e2b-agent',
    'version': '0.0.1',
    'description': 'API for interacting with Agent',
    'long_description': 'None',
    'author': 'e2b',
    'author_email': 'hello@e2b.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
