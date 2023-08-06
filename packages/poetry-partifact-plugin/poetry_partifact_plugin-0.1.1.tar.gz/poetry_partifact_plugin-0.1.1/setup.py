# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_partifact_plugin']

package_data = \
{'': ['*']}

install_requires = \
['partifact>=0.2.0,<0.3.0']

entry_points = \
{'poetry.application.plugin': ['poetry-partifact-plugin = '
                               'poetry_partifact_plugin.plugin:PartifactPlugin']}

setup_kwargs = {
    'name': 'poetry-partifact-plugin',
    'version': '0.1.1',
    'description': 'A poetry plugin that configures AWS CodeArtifact',
    'long_description': '## POETRY-PARTIFACT-PLUGIN\n\nThis project is a poetry plugin that wraps the `poetry add/install` commands and adds some logic\nthat will authenticate to AWS CodeArtifact under the hood.\n\nBefore any poetry `add` or `install` commands are run, this plugin will check the `pyproject.toml` file\nfor any codeartifact sources.\n\nIt is looking for the first `tool.poetry.source` block that contains `.codeartifact.` in its url. \nThe required fields are "url" and "name."\n\nIf the tool doesn\'t find any valid source blocks, nothing happens.\n\n## Configuration\n\nCreate a `tool.poetry.source` block in your `pyproject.toml` file, then set the "url" to the CodeArtifact repository url, and set the "name" to the id of the AWS profile you\'ll be using to authenticate.\n\nHere\'s an example of a valid `tool.poetry.source` block (the `default=true` is optional):\n```yaml\n[[tool.poetry.source]]\nname = "<your-aws-profile-name>"\nurl = "https://<your-domain-name>-<your-project-id>.d.codeartifact.<your-region>.amazonaws.com/pypi/<your-repo-name>/simple/"\ndefault = true\n```\n\n## Installation\n\nTo install the plugin, run this command:\n\n```shell\npoetry self add poetry-partifact-plugin\n```\n\n## Uninstallation\n\nTo remove the plugin, run this command:\n\n```shell\npoetry self remove poetry-partifact-plugin\n```\n\n## Under the Hood\n\nOnce the plugin has gotten your repository url and the name of the AWS profile you\'ll be using, it  uses the AWS profile credentials located at `~/.aws/credentials` to make an API request to your AWS CodeArtifact repository.\n\nIf this request is successful, a short-lived token will be returned that will grant temporary access.\nThis token is set as a [poetry environment variable](https://python-poetry.org/docs/configuration/#using-environment-variables) and allows poetry to seamlessly authenticate to the repository.\n\n## Dependencies\n\n* [partifact](https://github.com/Validus-Risk-Management/partifact)\n\n## License \nCopyright 2023 Amino Inc.\n\n   Licensed under the Apache License, Version 2.0 (the "License");\n   you may not use this file except in compliance with the License.\n   You may obtain a copy of the License at\n\n       http://www.apache.org/licenses/LICENSE-2.0\n\n   Unless required by applicable law or agreed to in writing, software\n   distributed under the License is distributed on an "AS IS" BASIS,\n   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n   See the License for the specific language governing permissions and\n   limitations under the License.',
    'author': 'Amino Engineering Team',
    'author_email': 'eng@amino.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aminohealth/poetry-partifact-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
