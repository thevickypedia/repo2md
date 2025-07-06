# repo2md

`repo2md` is a python module to convert GitHub repositories into Markdown files.

![Python][label-pyversion]

**Platform Supported**

![Platform][label-platform]

**Deployments**

[![pypi][label-actions-pypi]][gha_pypi]

[![Pypi][label-pypi]][pypi]
[![Pypi-format][label-pypi-format]][pypi-files]
[![Pypi-status][label-pypi-status]][pypi]

## Installation

```shell
pip install repo2md
```

## Usage

```python
import os
import dotenv

import repo2md

repo2md.IGNORE_DIRECTORIES.append("docs_gen")
repo2md.IGNORE_LIST.append("docs_gen")

dotenv.load_dotenv(".env", override=True)

repo2md.convert_repo_to_md(
    repo_name="Jarvis",
    git_owner="thevickypedia",
    git_token=os.getenv("GIT_TOKEN"),
)
```

#### CLI

```shell
repo2md --help
```
> _The CLI exposes fewer options than using the module directly in code._

## Coding Standards
Docstring format: [`Google`][google-docs] <br>
Styling conventions: [`PEP 8`][pep8] and [`isort`][isort]

## [Release Notes][release-notes]
**Requirement**
```shell
python -m pip install gitverse
```

**Usage**
```shell
gitverse-release reverse -f release_notes.rst -t 'Release Notes'
```

## Linting

**Requirement**
```shell
python -m pip install pre-commit
```

**Usage**
```shell
pre-commit run --all-files
```

## Pypi Package
[![pypi-module][label-pypi-package]][pypi-repo]

[https://pypi.org/project/repo2md/][pypi]

## License & copyright

&copy; Vignesh Rao

Licensed under the [MIT License][license]

[//]: # (Labels)

[3.11]: https://docs.python.org/3/whatsnew/3.11.html
[license]: https://github.com/thevickypedia/repo2md/blob/main/LICENSE
[google-docs]: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[pep8]: https://www.python.org/dev/peps/pep-0008/
[isort]: https://pycqa.github.io/isort/
[samples]: https://github.com/thevickypedia/repo2md/tree/main/samples

[label-actions-pypi]: https://github.com/thevickypedia/repo2md/actions/workflows/python-publish.yaml/badge.svg
[label-pypi]: https://img.shields.io/pypi/v/repo2md
[label-pypi-format]: https://img.shields.io/pypi/format/repo2md
[label-pypi-status]: https://img.shields.io/pypi/status/repo2md
[label-pypi-package]: https://img.shields.io/badge/Pypi%20Package-repo2md-blue?style=for-the-badge&logo=Python
[label-pyversion]: https://img.shields.io/badge/python-3.11%20%7C%203.12-blue
[label-platform]: https://img.shields.io/badge/Platform-Linux|macOS|Windows-1f425f.svg
[release-notes]: https://github.com/thevickypedia/repo2md/blob/main/release_notes.rst

[gha_pypi]: https://github.com/thevickypedia/repo2md/actions/workflows/python-publish.yml

[pypi]: https://pypi.org/project/repo2md
[pypi-files]: https://pypi.org/project/repo2md/#files
[pypi-repo]: https://packaging.python.org/tutorials/packaging-projects/
