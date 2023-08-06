# glean-cli

Command-line tools for interacting with Glean (https://glean.io).

Glean is currently in closed beta and the CLI is under active development.

## Development

During local development, you likely want to point the CLI at your local
Glean web server. You can do so with the following enviroment variable:

```bash
export GLEAN_CLI_BASE_URI=http://localhost:5000
```

You should work with the Glean CLI in its own virtual enviroment. In this
new environment, ensure you have `pip`, then do `pip install build` to get
the correct build tool.

The Glean CLI is a project built by `setuptools`. You can package it for
publish with `python -m build`, or link it for local development by running
`pip install --editable .` in the root folder of this repo.

Once installed as an editable package, run `glean --help` to use it.
