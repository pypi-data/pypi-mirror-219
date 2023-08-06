# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli', 'cli.commands', 'cli.commands.human', 'cli.infra']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'loguru==0.6.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'rich>=13.4.2,<14.0.0',
 'scaleway>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['scwgw = cli.cli:main']}

setup_kwargs = {
    'name': 'scw-gateway',
    'version': '0.6.1',
    'description': 'CLI to deploy and manage a self-hosted Kong gateway on Scaleway Serverless Ecosystem',
    'long_description': '# <img src="https://raw.githubusercontent.com/scaleway/serverless-gateway/main/logo.png" height="32"/> Scaleway Serverless Gateway\n\n[![PyPI version](https://badge.fury.io/py/scw-gateway.svg)](https://badge.fury.io/py/scw-gateway)\n[![Documentation Status](https://readthedocs.org/projects/serverless-gateway/badge/?version=latest)](https://serverless-gateway.readthedocs.io/en/latest/?badge=latest)\n[![Build status](https://github.com/scaleway/serverless-gateway/actions/workflows/build.yml/badge.svg)](https://github.com/scaleway/serverless-gateway/actions/workflows/build.yml/badge.svg)\n\nThe Scaleway Serverless Gateway is a self-hosted API gateway that runs on Scaleway [Serverless Containers](https://www.scaleway.com/en/serverless-containers/).\n\nIt lets you manage routing from a single base URL, as well as handle transversal concerns such as CORS and authentication.\n\nIt is built on [Kong Gateway](https://docs.konghq.com/gateway/latest/), giving you access to the [Kong plugin ecosystem](https://docs.konghq.com/hub/) to customize your deployments.\n\nYou can read all about it in [this blog post](https://www.scaleway.com/en/blog/api-gateway-early-access/).\n\nIf you would like to join in the discussion on how we continue developing the project, or give us feedback, then join us on the [#api-gateway-beta](https://app.slack.com/client/T7YEXCR7X/C05H07VBKJ4) channel on the Scaleway Community Slack.\n\n## 📃 Contents\n\n\nPlease see [the docs](https://serverless-gateway.readthedocs.io) for full documentation and features.\n\n## 💻 Quickstart\n\nTo deploy your gateway you need to install and configure the [Scaleway CLI](https://github.com/scaleway/scaleway-cli), and the [Gateway CLI](https://pypi.org/project/scw-gateway/) via [`pip`](https://pip.pypa.io/en/stable/index.html):\n\n```console\npip install scw-gateway\n```\n\nOnce done, the following steps can be run from the root of the project, and will deploy the gateway as a Serverless Container in your Scaleway account.\n\nThe gateway image itself is packaged via our public [Serverless Gateway Docker image](https://hub.docker.com/r/scaleway/serverless-gateway).\n\n### Deploy your gateway\n\nTo deploy your gateway, you can run:\n\n```console\nscwgw infra deploy\n```\n\nFor more information on the deployment process, see the [deployment docs](https://serverless-gateway.readthedocs.io/en/latest/deployment.html).\n\n### Add a route\n\nTo check your gateway is working, you can add and remove a route:\n\n```console\n# Check no routes are configured initially\nscwgw route ls\n\n# Check the response directly from a given URL\nTARGET_URL=http://worldtimeapi.org/api/timezone/Europe/Paris\ncurl $TARGET_URL\n\n# Add a route to this URL in your gateway\nscwgw route add /time $TARGET_URL\n\n# List routes to see that it\'s been configured\nscwgw route ls\n\n# Curl the URL via the gateway\nGATEWAY_ENDPOINT=$(scwgw infra endpoint)\ncurl https://${GATEWAY_ENDPOINT}/time\n```\n\n### Delete your gateway\n\nTo delete your gateway, you can run:\n\n```console\nscwgw infra delete\n```\n\n## 🎓 Contributing\n\nWe welcome all contributions to our open-source projects, please see our [contributing guidelines](./.github/CONTRIBUTING.md).\n\nDo not hesitate to raise issues and pull requests we will have a look at them.\n\n## 📬 Reach us\n\nWe love feedback. Feel free to:\n\n- Open a [Github issue](https://github.com/scaleway/serverless-gateway/issues/new)\n- Send us a message on the [Scaleway Slack community](https://slack.scaleway.com/), in the [#serverless-functions](https://scaleway-community.slack.com/app_redirect?channel=serverless-functions) channel.\n',
    'author': 'Simon Shillaker',
    'author_email': 'sshillaker@scaleway.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scaleway/serverless-gateway',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
