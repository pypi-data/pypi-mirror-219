# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wsrouter']

package_data = \
{'': ['*'], 'wsrouter': ['static/websocket.js']}

install_requires = \
['boltons>=21.0.0', 'orjson>=3.7.1', 'shortuuid>=1.0.9', 'starlette>=0.20.1']

setup_kwargs = {
    'name': 'wsrouter',
    'version': '0.8.3',
    'description': 'Starlette Shared WebSocket Endpoint',
    'long_description': '# WebSocket Router for Starlette\n\nThis package acts as a websocket message router for [Starlette](https://github.com/encode/starlette)\n[WebSocket](https://www.starlette.io/websockets/) connections, permitting socket sharing for\nmultiple client-server connections.\n\nFor installation and usage, [see the documentation](https://selcouth.gitlab.io/wsrouter).\n',
    'author': 'David Morris',
    'author_email': 'gypsysoftware@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/selcouth/wsrouter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
