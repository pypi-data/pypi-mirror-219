<!--
SPDX-FileCopyrightText: 2023 Alex Lemna <git@alexanderlemna.com>

SPDX-License-Identifier: CC0-1.0
-->

# Developer notes

*Reference: https://duarteocarmo.com/blog/opinionated-python-boilerplate*

## Create virtual environment

- `python3.10 -m venv .venv --upgrade-deps --prompt py3.10`
- activate the virtual environment (depends on platform)
- install auldcommons
    - in production: `python -m pip install -r requirements.txt --require-hashes`
    - in development: `python -m pip install -r requirements.txt -r requirements-dev.txt --isolated --require-hashes --require-virtualenv`

## Dependencies

*Reference: [link](https://hynek.me/til/pip-tools-and-pyproject-toml/)*
*Reference: [link](https://hynek.me/articles/python-recursive-optional-dependencies/)*

manage dependencies

- `python -m piptools compile --output-file requirements.txt pyproject.toml`
- `python -m piptools compile --extra dev --output-file requirements-dev.txt pyproject.toml`

update dependencies

- the same commands as above, but with the `--upgrade` flag. 
    - *"If pip-compile finds an existing `requirements.txt` file that fulfils the dependencies then no changes will be made, even if updates are available. To force pip-compile to update all packages in an existing `requirements.txt`, run `pip-compile --upgrade`." (source: [official README on GitHub](https://github.com/jazzband/pip-tools#updating-requirements))*


sync virtual environment and dependencies

- `pip-sync requirements.txt requirements-dev.txt` or `python -m piptools sync requirements.txt requirements-dev.txt` (equivalent)`
    - may need to run twice, if pip-tools itself needs to be reinstalled. It'll error out the first time, and then work the second time.
- `python -m pip check`

## Format

black

- Honestly, just see ask `black --help`. I just set up VS Code to autoformat with `black` everytime I save. (see the `.vscode/settings.json` file)

isort

- `isort . --check --diff` to check to see if imports are correctly sorted within this project

reuse

- `reuse lint`
- `reuse annotate --copyright="NAME <EMAIL>" --license="LICENSE" PATH`

## Document

**reuse** can produce an SPDX Software Bill of Materials

- `reuse spdx --output reuse.spdx`

## Build

editable

- `pip install -e . --isolated --require-hashes --require-virtualenv`

## Test

- `pytest`

## Publish

*Reference: https://twine.readthedocs.io/en/stable/*

git tag for release

- `<!-- TODO -->` 
    - *I just use VS Code, too lazy to look up the CLI git command right now. Question: Does `setuptools_scm` require it to be an annotated tag, or is a lightweight tag sufficient?*

build and publish to TestPyPI

- `python -m build`
- `twine upload -r testpypi dist/*`

test for release

- - `<!-- TODO -->` 
    - *Get the install command from Test PyPI*
    - *How to automate this on OpenBSD?*
- `pytest`

if tests pass, publish to PyPI

- `twine upload dist/*`
    - You'll be prompted for username and password
