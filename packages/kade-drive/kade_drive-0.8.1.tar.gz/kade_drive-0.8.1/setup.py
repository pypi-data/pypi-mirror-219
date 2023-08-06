# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kade_drive', 'kade_drive.core', 'kade_drive.tests']

package_data = \
{'': ['*']}

install_requires = \
['message-system>=0.1.2,<0.2.0', 'rpyc==5.3.1', 'typer==0.9.0']

entry_points = \
{'console_scripts': ['cli = kade_drive.cli:start_cli',
                     'server = kade_drive.server:start',
                     'test_store = kade_drive.test_store_file:test_store_df']}

setup_kwargs = {
    'name': 'kade-drive',
    'version': '0.8.1',
    'description': 'distributed file system based on kademlia dht',
    'long_description': '![Python Version](https://img.shields.io/badge/Python-3.10-blue)\n![Code Style](https://img.shields.io/badge/Code%20Style-Black-black)\n![Poetry Version](https://img.shields.io/badge/Poetry-1.3.1-blue)\n![Docker Support](https://img.shields.io/badge/Docker-Supported-brightgreen?logo=docker)\n[![Docker Pulls](https://badgen.net/docker/pulls/joramas/kade-drive?icon=docker&label=pulls)](https://hub.docker.com/r/joramas/kade-drive/)\n[![Docker Stars](https://badgen.net/docker/stars/joramas/kade-drive?icon=docker&label=stars)](https://hub.docker.com/r/joramas/kade-drive/)\n[![Docker Image Size](https://badgen.net/docker/size/joramas/kade-drive?icon=docker&label=image%20size)](https://hub.docker.com/r/joramas/kade-drive/)\n![Visits](https://badges.pufler.dev/visits/geeksLabTech/kade-drive)\n![Contributors](https://img.shields.io/github/contributors/geeksLabTech/kade-drive)\n![Release Version](https://img.shields.io/github/v/release/geeksLabTech/kade-drive)\n![Documentation](https://img.shields.io/badge/docs-available-brightgreen)\n![Package Version](https://img.shields.io/pypi/v/kade-drive)\n![Downloads](https://img.shields.io/pypi/dm/kade-drive)\n![Release Date](https://img.shields.io/github/release-date/geeksLabTech/kade-drive)\n![Code Size](https://img.shields.io/github/languages/code-size/geeksLabTech/kade-drive)\n\nDistributed file system based on <https://github.com/bmuller/kademlia> for the final project of distributed systems\n\n## Documentation\n\n<https://geekslabtech.github.io/kade-drive/>\n\n## Basic Usage\n\n- Clone the repo and run `poetry install`\n- Run `poetry run server` in one pc or several pc in a local network\n- Run `poetry run cli` in any pc of the network and start playing with the system\n\n### Usage with docker\n\n- Build the image with `make docker` or pull it from docker.hub `docker pull joramas/kade-drive:latest`\n- Run `make shell` to start the Docker container with an interactive Bash shell\n- Now you can run `poetry run server` to start a server or `poetry run cli`\n\n## Installation\n\n```console\npip install kade-drive\n```\n\n## Server\n\n```Python\nfrom kade_drive.server import start_server\n\nstart_server()\n```\n\n## Client\n\n### Note: Make sure that there exist at least a server in the local network\n\n```Python\nfrom kade_drive.cli import ClientSession\n\nclient = ClientSession()\nclient.connect()\nresponse, _ = client.put(4, 5)\n# If true, it means that the value was setted correctly, false otherwise\nassert response is True\nvalue, _ = client.get(4)\nassert value == 5\n```\n\n### Tests\n\nTo run tests make shure that there is at least one server in the network.\n',
    'author': 'DanielUH2019',
    'author_email': 'danielcardenascabrera2016@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
