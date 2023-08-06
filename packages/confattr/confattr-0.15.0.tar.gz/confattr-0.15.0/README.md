Config Attributes

A python library to read and write config files
with a syntax inspired by vimrc and ranger config.

Documentation: https://erzo.gitlab.io/confattr/latest


## Running the tests

I am using [mypy](https://www.mypy-lang.org/) for static type checking and [pytest](https://docs.pytest.org/en/latest/) for dynamic testing.
[tox](https://tox.wiki/en/latest/) creates a virtual environment and installs all dependencies for you.
You can install tox with [pipx](https://pypa.github.io/pipx/) (`pipx install tox`).

```bash
$ tox
```

In order to make tox work without an internet connection install [devpi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html):

```bash
$ pipx install devpi-server
$ devpi-init
$ devpi-gen-config
$ su
# cp gen-config/devpi.service /etc/systemd/system/
# systemctl start devpi.service
# systemctl enable devpi.service
```

and add the following line to your bashrc:

```bash
export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
```
