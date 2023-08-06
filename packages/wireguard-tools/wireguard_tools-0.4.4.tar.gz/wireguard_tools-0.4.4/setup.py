# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wireguard_tools']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0', 'pyroute2>=0.7.3,<0.8.0', 'segno>=1.5.2,<2.0.0']

entry_points = \
{'console_scripts': ['wg-py = wireguard_tools.cli:main']}

setup_kwargs = {
    'name': 'wireguard-tools',
    'version': '0.4.4',
    'description': 'Pure python reimplementation of wireguard-tools',
    'long_description': '# WireGuard-tools\n\nPure Python reimplementation of wireguard-tools with an aim to provide easily\nreusable library functions to handle reading and writing of\n[WireGuard®](https://www.wireguard.com/) configuration files as well as\ninteracting with WireGuard devices, both in-kernel through the Netlink API and\nuserspace implementations through the cross-platform UAPI API.\n\n\n## Installation/Usage\n\n```sh\n    pipx install wireguard-tools\n    wg-py --help\n```\n\nImplemented `wg` command line functionality,\n\n- [x] show - Show configuration and device information\n- [x] showconf - Dump current device configuration\n- [ ] set - Change current configuration, add/remove/change peers\n- [x] setconf - Apply configuration to device\n- [ ] addconf - Append configuration to device\n- [x] syncconf - Synchronizes configuration with device\n- [x] genkey, genpsk, pubkey - Key generation\n\n\nAlso includes some `wg-quick` functions,\n\n- [ ] up, down - Create and configure WireGuard device and interface\n- [ ] save - Dump device and interface configuration\n- [x] strip - Filter wg-quick settings from configuration\n\n\nNeeds root (sudo) access to query and configure the WireGuard devices through\nnetlink. But root doesn\'t know about the currently active virtualenv, you may\nhave to pass the full path to the script in the virtualenv, or use\n`python3 -m wireguard_tools`\n\n```sh\n    sudo `which wg-py` showconf <interface>\n    sudo /path/to/venv/python3 -m wireguard_tools showconf <interface>\n```\n\n\n## Library usage\n\n### Parsing WireGuard keys\n\nThe WireguardKey class will parse base64-encoded keys, the default base64\nencoded string, but also an urlsafe base64 encoded variant. It also exposes\nboth private key generating and public key deriving functions. Be sure to pass\nany base64 or hex encoded keys as \'str\' and not \'bytes\', otherwise it will\nassume the key was already decoded to its raw form.\n\n```python\nfrom wireguard_tools import WireguardKey\n\nprivate_key = WireguardKey.generate()\npublic_key = private_key.public_key()\n\n# print base64 encoded key\nprint(public_key)\n\n# print urlsafe encoded key\nprint(public_key.urlsafe)\n\n# print hexadecimal encoded key\nprint(public_key.hex())\n```\n\n### Working with WireGuard configuration files\n\nThe WireGuard configuration file is similar to, but not quite, the INI format\nbecause it has duplicate keys for both section names (i.e. [Peer]) as well as\nconfiguration keys within a section. According to the format description,\nAllowedIPs, Address, and DNS configuration keys \'may be specified multiple\ntimes\'.\n\n```python\nfrom wireguard_tools import WireguardConfig\n\nwith open("wg0.conf") as fh:\n    config = WireguardConfig.from_wgconfig(fh)\n```\n\nAlso supported are the "Friendly Tags" comments as introduced by\nprometheus-wireguard-exporter, where a `[Peer]` section can contain\ncomments which add a user friendly description and/or additional attributes.\n\n```\n[Peer]\n# friendly_name = Peer description for end users\n# friendly_json = {"flat"="json", "dictionary"=1, "attribute"=2}\n...\n```\n\nThese will show up as additional `friendly_name` and `friendly_json` attributes\non the WireguardPeer object.\n\nWe can also serialize and deserialize from a simple dict-based format which\nuses only basic JSON datatypes and, as such, can be used to convert to various\nformats (i.e. json, yaml, toml, pickle) either to disk or to pass over a\nnetwork.\n\n```python\nfrom wireguard_tools import WireguardConfig\nfrom pprint import pprint\n\ndict_config = dict(\n    private_key="...",\n    peers=[\n        dict(\n            public_key="...",\n            preshared_key=None,\n            endpoint_host="remote_host",\n            endpoint_port=5120,\n            persistent_keepalive=30,\n            allowed_ips=["0.0.0.0/0"],\n            friendly_name="Awesome Peer",\n        ),\n    ],\n)\nconfig = WireguardConfig.from_dict(dict_config)\n\ndict_config = config.asdict()\npprint(dict_config)\n```\n\nFinally, there is a `to_qrcode` function that returns a segno.QRCode object\nwhich contains the configuration. This can be printed and scanned with the\nwireguard-android application. Careful with these because the QRcode exposes\nan easily captured copy of the private key as part of the configuration file.\nIt is convenient, but definitely not secure.\n\n```python\nfrom wireguard_tools import WireguardConfig\nfrom pprint import pprint\n\ndict_config = dict(\n    private_key="...",\n    peers=[\n        dict(\n            public_key="...",\n            preshared_key=None,\n            endpoint_host="remote_host",\n            endpoint_port=5120,\n            persistent_keepalive=30,\n            allowed_ips=["0.0.0.0/0"],\n        ),\n    ],\n)\nconfig = WireguardConfig.from_dict(dict_config)\n\nqr = config.to_qrcode()\nqr.save("wgconfig.png")\nqr.terminal(compact=True)\n```\n\n\n### Working with WireGuard devices\n\n```python\nfrom wireguard_tools import WireguardDevice\n\nifnames = [device.interface for device in WireguardDevice.list()]\n\ndevice = WireguardDevice.get("wg0")\n\nwgconfig = device.get_config()\n\ndevice.set_config(wgconfig)\n```\n\n## Bugs\n\nThe setconf/syncconf implementation is not quite correct. They currently use\nthe same underlying set of operations but netlink-api\'s `set_config`\nimplementation actually does something closer to syncconf, while the uapi-api\nimplementation matches setconf.\n\nThis implementation has only been tested on Linux where we\'ve only actively\nused a subset of the available functionality, i.e. the common scenario is\nconfiguring an interface only once with just a single peer.\n\n\n## Licenses\n\nwireguard-tools is MIT licensed\n\n    Copyright (c) 2022-2023 Carnegie Mellon University\n\n    Permission is hereby granted, free of charge, to any person obtaining a copy of\n    this software and associated documentation files (the "Software"), to deal in\n    the Software without restriction, including without limitation the rights to\n    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies\n    of the Software, and to permit persons to whom the Software is furnished to do\n    so, subject to the following conditions:\n\n    The above copyright notice and this permission notice shall be included in all\n    copies or substantial portions of the Software.\n\n    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n    SOFTWARE.\n\n`wireguard_tools/curve25519.py` was released in the public domain\n\n    Copyright Nicko van Someren, 2021. This code is released into the public domain.\n    https://gist.github.com/nickovs/cc3c22d15f239a2640c185035c06f8a3\n\n"WireGuard" is a registered trademark of Jason A. Donenfeld.\n',
    'author': 'Carnegie Mellon University',
    'author_email': 'satya+group@cs.cmu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cmusatyalab/wireguard-tools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
