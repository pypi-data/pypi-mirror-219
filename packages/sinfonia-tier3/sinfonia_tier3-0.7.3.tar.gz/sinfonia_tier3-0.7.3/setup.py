# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sinfonia_tier3']

package_data = \
{'': ['*'], 'sinfonia_tier3': ['openapi/*']}

install_requires = \
['attrs>=22.1.0',
 'importlib-resources>=5.0,<6.0',
 'openapi-core>=0.17.2,<0.18.0',
 'pyroute2>=0.7.3,<0.8.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'wireguard-tools>=0.4.1,<0.5.0',
 'wireguard4netns>=0.1.3,<0.2.0',
 'xdg>=5.1.1,<6.0.0',
 'yarl>=1.7.2,<2.0.0']

entry_points = \
{'console_scripts': ['sinfonia-tier3 = sinfonia_tier3.cli:main']}

setup_kwargs = {
    'name': 'sinfonia-tier3',
    'version': '0.7.3',
    'description': 'Tier 3 component of the Sinfonia system',
    'long_description': "# Sinfonia\n\nManages discovery of nearby cloudlets and deployment of backends for\nedge-native applications.\n\nThe framework is a 3 tiered system. Tier 1 is located in the cloud and tracks\navailability of the Tier 2 instances running on the edge of the network\n(cloudlets) where backends can be deployed. Tier 3 is the client application\nthat mediates the discovery and deployment process for edge-native\napplications.\n\nThis repository implements an example Tier3 client which can be used both as a\ncommand-line application and as a Python library.\n\n\n## Installation\n\nYou probably don't need to install this directly, most of the time it should\nget installed as a dependency of whichever edge-native application is using\nthe Sinfonia framework to discover nearby cloudlets.\n\nBut if you want to run the standalone command-line application, you can install\nthis with installable with `pipx install sinfonia-tier3` or\n`pip install [--user] sinfonia-tier3`.\n\n\n## Usage\n\nThe `sinfonia-tier3` application would normally be called by any edge-native\napplication that uses the Sinfonia framework to deploy its application specific\nbackend on a nearby cloudlet.\n\nThe information needed by the application are the URL of a Tier1 instance\nand the UUID identifying the required backend. The remainder of the arguments\nconsist of the actual frontend application and arguments that will be launched\nin an seperate network namespace connecting back to the deployed backend.\n\n    $ sinfonia-tier3 <tier1-url> <uuid> <frontend-app> <args...>\n\nAn example application with UUID:00000000-0000-0000-0000-000000000000 (or the\nconvenient alias 'helloworld') starts an nginx server that will be accessible\nwith the hostname 'helloworld'.\n\n    $ sinfonia-tier3 https://tier1.server.url/ helloworld /bin/sh\n    sinfonia$ curl -v http://helloworld/\n    ...\n    sinfonia$ exit\n\nWhen the frontend application exits, the network namespace and WireGuard tunnel\nare cleaned up. Any resources on the cloudlet will be automatically released\nonce the Sinfonia-tier2 instance notices the VPN tunnel has been idle.\n\n\n## Installation from this source repository\n\nYou need a recent version of `poetry`\n\n    $ pip install --user pipx\n    $ ~/.local/bin/pipx ensurepath\n    ... possibly restart shell to pick up the right PATH\n    $ pipx install poetry\n\nAnd then use poetry to install the necessary dependencies,\n\n    $ git clone https://github.com/cmusatyalab/sinfonia-tier3.git\n    $ cd sinfonia-tier3\n    $ poetry install\n    $ poetry run sinfonia-tier3 ...\n    ... or\n    $ poetry shell\n    (env)$ sinfonia-tier3 ...\n\n\n## Why do we need a sudo password when deploying\n\nActually you should not need a password if `wireguard4netns` works correctly\nBut if for some reason it fails to create the tuntap device and launch\nwireguard-go, the code will fall back on the older `sudo` implementation.\n\nThe older `sudo` implementation uses the in-kernel Wireguard implementation and\nneeds root access to create and configure the WireGuard device and endpoint.\nAll of the code running as root is contained in\n[src/sinfonia_tier3/root_helper.py](https://github.com/cmusatyalab/sinfonia-tier3/blob/main/src/sinfonia_tier3/root_helper.py)\n\nIt runs the equivalent of the following.\n\n```sh\n    ip link add wg-tunnel type wireguard\n    wg set wg-tunnel private-key <private-key> peer <public-key> endpoint ...\n    ip link set dev wg-tunnel netns <application network namespace>\n```\n",
    'author': 'Carnegie Mellon University',
    'author_email': 'satya+group@cs.cmu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cmusatyalab/sinfonia-tier3',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
