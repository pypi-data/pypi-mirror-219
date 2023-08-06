# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['promptlink']

package_data = \
{'': ['*'], 'promptlink': ['static/*']}

install_requires = \
['Jinja2',
 'functions-framework',
 'google-cloud-functions',
 'google-cloud-pubsub',
 'google-cloud-storage',
 'pyyaml']

setup_kwargs = {
    'name': 'promptlink',
    'version': '0.1.3',
    'description': 'Simplify user authentication and secure access from anywhere with customizable prompts and temporary links.',
    'long_description': '# PromptLink\n\n[![PyPI version](https://badge.fury.io/py/promptlink.svg)](https://badge.fury.io/py/promptlink)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nSimplify user authentication and secure access from anywhere with temporary links.\n\nPromptLink is a Python package that allows you to streamline user authentication and enable secure access to your application from anywhere. It provides a seamless way to generate temporary links for user authentication, without relying on specific web frameworks. A Google Cloud Function is set up to ensure a secure temporary link for authentication.\n\n## Key Features\n\n- **Easy and secure**: Generate secure temporary links to enable easy secure access from anywhere.\n- **Versatile Integration**: Works across various application types, not limited to web applications.\n\n## Installation\n\nYou can install PromptLink using pip:\n```shell\npip install promptlink\n```\nAlternatively, if you are using Poetry (recommended), you can install it as follows:\n```shell\npoetry add promptlink\n```\n\n## Usage\n\nHere\'s a basic example of using PromptLink:\n\n```python\nfrom promptlink import Authenticator\n\n\nwith Authenticator(send_link_callback=lambda l: print(f"URL: {l}")) as authenticator:\n    # The code in this block is executed after the link has been accessed \n    # in order to avoid authentication timeouts\n    print("Setting up authentication...")\n    authenticator.authenticate(lambda s: s == "12345678")\n    # Below statements will be reached after \'12345678\' was input on the webpage prompt\n    print("Finished")\n```\n\n## GCP permission requirements\nThe following permissions are needed for this library:\n- Permissions to create Storage buckets and objects\n- Permissions to set up a Pub/Sub topic and subscriptions\n- Permissions to deploy a Cloud Function  \n\nThe library will attempt to use the default service account.\nAny resources created will be named \'promptlink-\' followed by a random UUID, so that collision with existing resources is extremely unlikely.\n\n## License\nThis project is licensed under the MIT License. See the LICENSE file for details.\n',
    'author': 'Stéphane Thibaud',
    'author_email': 'snthibaud@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
