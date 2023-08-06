## POETRY-PARTIFACT-PLUGIN

This project is a poetry plugin that wraps the `poetry add/install` commands and adds some logic
that will authenticate to AWS CodeArtifact under the hood.

Before any poetry `add` or `install` commands are run, this plugin will check the `pyproject.toml` file
for any codeartifact sources.

It is looking for the first `tool.poetry.source` block that contains `.codeartifact.` in its url. 
The required fields are "url" and "name."

If the tool doesn't find any valid source blocks, nothing happens.

## Configuration

Create a `tool.poetry.source` block in your `pyproject.toml` file, then set the "url" to the CodeArtifact repository url, and set the "name" to the id of the AWS profile you'll be using to authenticate.

Here's an example of a valid `tool.poetry.source` block (the `default=true` is optional):
```yaml
[[tool.poetry.source]]
name = "<your-aws-profile-name>"
url = "https://<your-domain-name>-<your-project-id>.d.codeartifact.<your-region>.amazonaws.com/pypi/<your-repo-name>/simple/"
default = true
```

## Installation

To install the plugin, run this command:

```shell
poetry self add poetry-partifact-plugin
```

## Uninstallation

To remove the plugin, run this command:

```shell
poetry self remove poetry-partifact-plugin
```

## Under the Hood

Once the plugin has gotten your repository url and the name of the AWS profile you'll be using, it  uses the AWS profile credentials located at `~/.aws/credentials` to make an API request to your AWS CodeArtifact repository.

If this request is successful, a short-lived token will be returned that will grant temporary access.
This token is set as a [poetry environment variable](https://python-poetry.org/docs/configuration/#using-environment-variables) and allows poetry to seamlessly authenticate to the repository.

## Dependencies

* [partifact](https://github.com/Validus-Risk-Management/partifact)

## License 
Copyright 2023 Amino Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.