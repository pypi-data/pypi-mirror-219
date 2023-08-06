# Contributing

## Setting up local development

Clone repository from GitHub:

```console
git clone https://github.com/kianmeng/xsget
cd xsget
```

To set up different Python environments, we need to install all supported
Python version using <https://github.com/pyenv/pyenv>. Once you've installed
Pyenv, install these additional Pyenv plugins:

```console
git clone https://github.com/pyenv/pyenv-doctor.git "$(pyenv root)/plugins/pyenv-doctor"
pyenv doctor

git clone https://github.com/pyenv/pyenv-update.git $(pyenv root)/plugins/pyenv-update
pyenv update
```

Run the command below to install all Python versions:

```console
pyenv install $(cat .python-version)
```

Install and upgrade required Python packages:

```console
pipenv install --dev
pipenv run playwright install
```

Spawn a shell in virtual environment for your development:

```console
pipenv shell
```

Show all available tox tasks:

```console
tox -av
...
default environments:
py37    -> testing against python3.7
py38    -> testing against python3.8
py39    -> testing against python3.9
py310   -> testing against python3.10
py311   -> testing against python3.11

additional environments:
cover   -> generate code coverage report in html
doc     -> generate sphinx documentation in html
gettext -> update pot/po/mo files
```

For code linting, we're using `pre-commit`:

```console
pre-commit install
pre-commit clean
pre-commit run --all-files
```

Or specific hook:

```console
pre-commit run pylint -a
```

## Create a Pull Request

Fork it at GitHub, <https://github.com/kianmeng/xsget/fork>

Create your feature branch:

```console
git checkout -b my-new-feature
```

Commit your changes:

```console
git commit -am 'Add some feature'
```

Push to the branch:

```console
git push origin my-new-feature
```

Create new Pull Request in GitHub.

## License

By contributing to xsget, you agree that your contributions will be licensed
under the LICENSE.md file in the root directory of this source tree.
